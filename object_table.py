import os
import pandas as pd
from biokbase.workspace.client import Workspace
ws = Workspace('https://kbase.us/services/ws')


#get data
def get_obj_data(obj_name):
 
 ws_name = os.environ['KB_WORKSPACE_ID']
 try:
   obj_id = ws.get_object_info3({'objects': [{'workspace': ws_name, 'name': obj_name}]})['paths'][0][0]
   return ws.get_objects([{"ref":obj_id}])[0]
 except:
    print "error"
    return False


def get_selected_metadata (obj_name):
    try:
      obj_meta_data = get_obj_data(obj_name)
      return obj_meta_data.get('info')[10]
    except:
        return False

def format_metadata(obj_name, keys):
    metadata = get_selected_metadata(obj_name)
    return [metadata[x] for x in keys]


def DataTable(df):
    """Display a pandas.DataFrame as jQuery DataTables"""
    import uuid
    from IPython.display import HTML
    # Generate random container name
    id_container = uuid.uuid1()
    output = """
<div id="datatable-container-{id_container}">
  <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/u/dt/dt-1.10.12/datatables.min.css"/>
  <script type="text/javascript" src="https://cdn.datatables.net/u/dt/dt-1.10.12/datatables.min.js"></script>
  <script type="text/javascript">
    (function () {{
      function tablify() {{
        if ( $().dataTable === undefined ) {{
          setTimeout(tablify, 100);
          return;
        }}
      $('#datatable-container-{id_container} table.datatable').dataTable();
      }}
      tablify();
    }})();
  </script>
  <!-- Insert table below -->
  {table}
</div>
    """.format(
        id_container=id_container,
        table=df.to_html(index=True, classes="datatable dataframe"))
    return HTML(output)


def get_objects_metadata_table(ws_name, object_type):
    #ws_name = os.environ['KB_WORKSPACE_ID']
    objects_in_workspace = ws.list_objects({'workspaces': [ws_name],
                 'type': object_type      
                })
    object_names = sorted ([j[1] for j in objects_in_workspace])

    d = dict()

    for object_name in object_names:
        metadata = get_selected_metadata(object_name)
        metadata_keys = metadata.keys()
        metadata_values = format_metadata (object_name, metadata_keys)
        object_pd = pd.Series(metadata_values,index = metadata_keys)
        d[object_name] = object_pd 

    df = pd.DataFrame(d)
    return df
