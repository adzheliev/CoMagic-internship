import ujson
from typing import List, Tuple
from enum import Enum

from uc_flow_nodes.schemas import NodeRunContext
from uc_flow_nodes.service import NodeService
from uc_flow_nodes.views import info, execute
from uc_flow_schemas import flow
from uc_flow_schemas.flow import Property, CredentialProtocol, RunState, DisplayOptions, OptionValue
from uc_http_requester.requester import Request


class Option(str, Enum):
    value_1 = 'Value_1'
    value_2 = 'Value_2'


class NodeType(flow.NodeType):
    id: str = '7ba71506-83f5-48a4-9181-fa3d89675e33'
    type: flow.NodeType.Type = flow.NodeType.Type.action
    name: str = 'alan_dzheliev_app'
    displayName: str = 'alan_dzheliev_app'
    icon: str = '<svg><text x="8" y="50" font-size="50">🤖</text></svg>'
    description: str = 'Application by Alan Dzheliev'
    properties: List[Property] = [
        Property(
            displayName='Переключатель',
            name='switcher_field',
            type=Property.Type.BOOLEAN,
            placeholder='Switcher placeholder',
            description='Switcher description',
            required=True,
            default='Test data',
        ),
        Property(
            displayName='Первое поле',
            name='first_field',
            type=Property.Type.OPTIONS,
            noDataExpression=True,
            displayOptions=DisplayOptions(
                show={
                    'switcher_field': [True]},
            ),
            options=[
                OptionValue(
                    name='Значение 1',
                    value='Value_1',
                    description='Значение 1',
                ),
                OptionValue(
                    name='Значение 2',
                    value='Value_2',
                    description='Значение 2',
                ),
            ],
        ),
        Property(
            displayName='Второе поле',
            name='second_field',
            type=Property.Type.OPTIONS,
            noDataExpression=True,
            displayOptions=DisplayOptions(
                show={
                    'switcher_field': [True]},
            ),
            options=[
                OptionValue(
                    name='Значение 1',
                    value='Value_1',
                    description='Значение 1',
                ),
                OptionValue(
                    name='Значение 2',
                    value='Value_2',
                    description='Значение 2',
                ),
            ],
        ),
        Property(
            displayName='Поле для ввода почты',
            name='email_field',
            type=Property.Type.STRING,
            noDataExpression=True,
            displayOptions=DisplayOptions(
                show={
                    'first_field': [
                        Option.value_1
                    ],
                    'second_field': [
                        Option.value_1
                    ],
                },
            ),
        ),
        Property(
            displayName='Поле для ввода даты и времени',
            name='date_time_field',
            type=Property.Type.DATETIME,
            noDataExpression=True,
            displayOptions=DisplayOptions(
                show={
                    'first_field': [
                        Option.value_2
                    ],
                    'second_field': [
                        Option.value_2
                    ],
                },
            ),
        ),  
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
