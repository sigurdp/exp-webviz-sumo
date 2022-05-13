from dash import html
from dash import Dash, Input, Output
from fmu.sumo.explorer import Explorer
from fmu.sumo.explorer import Case
from fmu.sumo.explorer import DocumentCollection
from webviz_config import WebvizPluginABC
import webviz_core_components as wcc
from io import BytesIO



class ListSurfacesPlugin(WebvizPluginABC):
    def __init__(
        self,
        app: Dash,
    ):
        super().__init__()

        self.set_callbacks(app)

    @property
    def layout(self) -> html.Div:
        return wcc.FlexBox([
            wcc.Frame(
                style={"flex": 1, "height": "90vh"},
                children=[
                    html.Button("Connect", id=self.uuid("connect_button")),
                    html.Br(),
                    html.Br(),
                    html.Button("GetBlob", id=self.uuid("getblob_button")),
                ],
            ),
            wcc.Frame(
                style={"flex": 5},
                children=[
                    html.Div(
                        id=self.uuid("info_div_1"),
                    ),
                    html.Div(
                        id=self.uuid("info_div_2"),
                    ),
                ],
            ),
        ])

    def set_callbacks(self, app: Dash) -> None:
        
        @app.callback(
            Output(self.uuid("info_div_1"), "children"),
            Input(self.uuid("connect_button"), "n_clicks"),
            prevent_initial_call=True,
        )
        def _connect_button_clicked(_n_clicks: int) -> list:
            print("CALLBACK _connect_button_clicked()")

            print("Connecting...")

            children = [html.U(html.B("Connect debug info:"))]

            try:
                sumo = Explorer(
                    env="dev",
                    token=None,
                    interactive=True,
                )

                all_fields: dict = sumo.get_fields()
                print("\nall_fields:")
                print(all_fields)

                children.extend([
                    html.P("all_fields"),
                    html.P(str(all_fields)),
                ])

                selected_field = list(all_fields)[0]
                my_cases: DocumentCollection = sumo.get_cases(fields=[selected_field])

                case_count = len(my_cases)
                outstr = f"\nmy_cases (count={case_count}, field={selected_field}):"
                print(outstr)
                children.append(html.P(outstr))
                for caseidx in range(case_count):
                    case: Case = my_cases[caseidx]
                    outstr = f"case {caseidx}: field={case.field_name}  case={case.case_name}  sumo_id={case.sumo_id}"
                    print(outstr)
                    children.append(html.P(outstr))

                children.append(html.P("Connect done"))

            except Exception as exc:
                return [
                    html.U(html.B("Exception occurred:")),
                    html.P(str(exc)),
                ]

            return children


        @app.callback(
            Output(self.uuid("info_div_2"), "children"),
            Input(self.uuid("getblob_button"), "n_clicks"),
            prevent_initial_call=True,
        )
        def _getblob_button_clicked(_n_clicks: int) -> list:
            print("CALLBACK _getblob_button_clicked()")

            print("Connecting...")

            children = [html.U(html.B("GetBlob debug info:"))]

            sumo_case_id = "0a4b8f65-2d32-91a9-c244-f54d69ea7bb8"

            try:
                sumo = Explorer(
                    env="dev",
                    token=None,
                    interactive=True,
                )

                case = sumo.get_case_by_id(sumo_case_id)

                outstr = f"field={case.field_name}  case={case.case_name}  sumo_id={case.sumo_id}"
                print(outstr)
                children.append(html.P(outstr))

                surface_collection = case.get_objects(
                    "surface",
                    iteration_ids=[0],
                    realization_ids=[0],
                )

                surf = surface_collection[0]
                blob_bytes: bytes = surf.blob
                byte_stream = BytesIO(blob_bytes)

                children.append(html.P("GetBlob done"))

            except Exception as exc:
                return [
                    html.U(html.B("Exception occurred:")),
                    html.P(str(exc)),
                ]

            return children
