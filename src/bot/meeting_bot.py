from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import BaseStorage, FSMContext
from aiogram.types import Message, ContentType, \
    CallbackQuery

import callbacks
from bot.states import BotStates
from keybords.select_keyboard import SelectKeyboard
from services.meeting_invite_service import MeetingInviteService
from services.meeting_service import MeetingService
from services.user_service import UserService
from utils.font_utils import FontUtils


class MeetingBot:
    _dispatcher: Dispatcher
    _bot: Bot
    _storage: BaseStorage

    def __init__(self, bot_token: str):
        bot = Bot(token=bot_token)
        self._bot = bot
        self._storage = MemoryStorage()
        self._dispatcher = Dispatcher(bot, storage=self._storage)

    @property
    def dispatcher(self):
        return self._dispatcher

    @property
    def bot(self):
        return self._bot

    def initialize_dispatcher(self):

        @self.dispatcher.message_handler(commands="start")
        async def start(msg: Message):
            UserService.register(msg.from_user)

        @self.dispatcher.message_handler(state='*', commands=["cancel", "done"])
        async def cancel_handler(message: Message, state: FSMContext):
            """
            Allow user to cancel any state
            """
            current_state = await state.get_state()
            if current_state is None:
                return

            await state.finish()
            await message.answer(f"Cancelled")

        @self.dispatcher.message_handler(content_types=[ContentType.CONTACT], state=BotStates.invite_state)
        async def get_contact(msg: Message, state: FSMContext):
            data = await state.get_data()
            meeting_id = data["meeting_id"]

            invite_service = MeetingInviteService(msg.from_user.id, msg.from_user.username)
            user_id = UserService.get_user_id(msg.contact.user_id)
            if user_id is None:
                await msg.answer(
                    f"Could not send invite\nUser {msg.contact.first_name} {msg.contact.last_name if msg.contact.last_name else ''} need start conversation with @YourMeetingManagerBot")
                return

            invite_service.send_invite(meeting_id, user_id)

            await self.bot.send_message(chat_id=msg.contact.user_id,
                                        text="You got invite to meeting. Write /myInvites to get it")
            await msg.answer(f"Invite was send to user")

        @self.dispatcher.message_handler(state=BotStates.invite_state)
        async def get_contact(msg: Message):
            await msg.answer(f"Send contact to invite it to meeting. Otherwise send /cancel or /done")

        @self.dispatcher.message_handler(commands=["invite"])
        async def set_invite_state(msg: Message):
            meeting_service = MeetingService(msg.from_user.id, msg.from_user.username)
            meetings = meeting_service.get_all()
            select_meeting_kb = SelectKeyboard(
                {meeting.title: {callbacks.invite_meeting_callback.KEY_MEETING_ID: meeting.id} for meeting in meetings},
                callbacks.invite_meeting_callback)
            await msg.answer("Select to which meeting you want to send invite",
                             reply_markup=select_meeting_kb.generate_markup())

        @self.dispatcher.message_handler(commands=["myInvites"])
        async def get_invites(msg: Message):

            meeting_service = MeetingService(msg.from_user.id, msg.from_user.username)
            invite_service = MeetingInviteService(msg.from_user.id, msg.from_user.username)
            invites = invite_service.get_unanswered()

            if len(invites) == 0:
                await self.bot.send_message(chat_id=msg.from_user.id, text="You have no unanswered invites")
                return

            for invite in invites:
                answer_keyboard = SelectKeyboard(
                    {
                        "Accept": {
                            callbacks.invite_answer_callback.KEY_MEETING_ID: invite.meetingId,
                            callbacks.invite_answer_callback.KEY_ANSWER: "acc"
                        },
                        "Reject": {
                            callbacks.invite_answer_callback.KEY_MEETING_ID: invite.meetingId,
                            callbacks.invite_answer_callback.KEY_ANSWER: "rej"
                        },
                    },
                    callbacks.invite_answer_callback)

                meeting = meeting_service.get(invite.meetingId)

                invite_text = f"{FontUtils.bold(meeting.title)}\n{'=' * 10}\n{FontUtils.italic(meeting.description)}\n\nStaring: {meeting.startDate}"

                await self.bot.send_message(
                    chat_id=msg.from_user.id,
                    text=invite_text,
                    reply_markup=answer_keyboard.generate_markup(),
                    parse_mode='Markdown'
                )

        @self.dispatcher.callback_query_handler(callbacks.invite_answer_callback.filter())
        async def answer_to_invite(call: CallbackQuery):
            meeting_id = callbacks.invite_answer_callback.parse_meeting_id(call.data)
            accepted = callbacks.invite_answer_callback.parse_accepted(call.data)

            invite_service = MeetingInviteService(call.from_user.id, call.from_user.username)
            if accepted:
                invite_service.accept_invite(meeting_id)
                await self.bot.send_message(chat_id=call.message.chat.id, text="Invite accepted\nYou can find meeting in webapp")
            else:
                invite_service.reject_invite(meeting_id)

            await self.bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        @self.dispatcher.callback_query_handler(callbacks.invite_meeting_callback.filter())
        async def set_state_invite_to_meeting(call: CallbackQuery):
            meeting_id = callbacks.invite_meeting_callback.parse_meeting_id(call.data)
            await BotStates.invite_state.set()

            state = self.dispatcher.current_state(chat=call.message.chat.id, user=call.from_user.id)
            await state.set_data({"meeting_id": meeting_id})

            meeting_service = MeetingService(call.from_user.id, call.from_user.username)
            meeting = meeting_service.get(meeting_id)

            new_message = f"{call.from_user.username}, send contact you want to invite to \"{meeting.title}\" meeting\nSend /done or /cancel, when finished"
            await self.bot.edit_message_text(text=new_message, chat_id=call.message.chat.id,
                                             message_id=call.message.message_id, reply_markup=None)
