import ujson
from typing import List, Tuple

from uc_flow_nodes.schemas import NodeRunContext
from uc_flow_nodes.service import NodeService
from uc_flow_nodes.views import info, execute
from uc_flow_schemas import flow
from uc_flow_schemas.flow import Property, CredentialProtocol, RunState
from uc_http_requester.requester import Request


class NodeType(flow.NodeType):
    id: str = '7ba71506-83f5-48a4-9181-fa3d89675e33'
    type: flow.NodeType.Type = flow.NodeType.Type.action
    name: str = 'alan_dzheliev_app'
    displayName: str = 'alan_dzheliev_app'
    icon: str = '<svg><text x="8" y="50" font-size="50">🤖</text></svg>'
    description: str = 'Application by Alan Dzheliev'
    properties: List[Property] = [
        Property(
            displayName='Тестовое поле',
            name='string_field',
            type=Property.Type.STRING,
            placeholder='String placeholder',
            description='String description',
            required=True,
            default='Test data',
        ),
        Property(
            displayName='Числовое поле',
            name='numeric_field',
            type=Property.Type.NUMBER,
            placeholder='Numeric placeholder',
            description='Numeric description',
            required=True,
            default='Test data',
        ),
        Property(
            displayName='String if OFF/numeric if ON',
            name='switcher_field',
            type=Property.Type.BOOLEAN,
            placeholder='Switcher placeholder',
            description='Switcher description',
            required=True,
            default='Test data',
        )
    ]


class InfoView(info.Info):
    class Response(info.Info.Response):
        node_type: NodeType


class ExecuteView(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        try:
            if json.node.data.properties.get('switcher_field') is not None:
                await json.save_result({
                    "result": int(json.node.data.properties['string_field']) + int(json.node.data.properties['numeric_field'])
                })
            else:
                await json.save_result({
                    "result": str(json.node.data.properties['string_field']) + str(json.node.data.properties['numeric_field'])
                })
            json.state = RunState.complete
        except Exception as e:
            self.log.warning(f'Error {e}')
            await json.save_error(str(e))
            json.state = RunState.error
        return json


class Service(NodeService):
    class Routes(NodeService.Routes):
        Info = InfoView
        Execute = ExecuteView
