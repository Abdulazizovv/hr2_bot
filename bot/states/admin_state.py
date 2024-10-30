from aiogram.dispatcher.filters.state import StatesGroup, State



class AdminState(StatesGroup):
    new_position_name = State()
    new_position_description = State()
    edit_position_name = State()
    edit_position_description = State()
    new_admin_id = State()