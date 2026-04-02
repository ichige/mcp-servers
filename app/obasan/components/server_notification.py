from nicegui import ui
from obasan.stores import phase

def server_notification():
    """
    MCPサーバからの通知メッセージ
    """
    # server status
    server_status = ui.input().props("readonly disable dense")
    server_status.bind_value(
        target_object=phase,
        target_name="state_message",
    )
    with server_status.add_slot('prepend'):
        ui.spinner(
            type='dots',
            size='xs',
            color='accent'
        ).bind_visibility(
            target_object=phase,
            target_name="is_pending",
        )