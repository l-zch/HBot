from dataclasses import dataclass
from discord import ButtonStyle, SelectOption
from discord.ui import View, Button, Select
from typing import List
from json import dumps

from Service.ButtonData import ButtonData
from Service.Label import Label


class Dashboard:

    def __init__(self):
        self.view = View()
        self.options = []

    def add_main_page_button(self, data: ButtonData):
        self.view.add_item(
            Button(
                label=data.label,
                style=ButtonStyle.success,
                custom_id=data.to_json(),
                disabled=False))
        return self

    def add_conductor(self, buttons_data: List[ButtonData]):
        for data in buttons_data:
            self.view.add_item(
                Button(
                    label=data.label,
                    style=ButtonStyle.success,
                    custom_id=data.to_json(),
                    disabled=data.disabled))
        return self

    def add_start_button(self, data: ButtonData):
        self.view.add_item(
            Button(
                label=data.label,
                style=ButtonStyle.success,
                custom_id=data.to_json(),
                disabled=False))
        return self

    def add_private_mode_button(self, data: ButtonData):
        self.view.add_item(
            Button(
                label=data.label,
                style=ButtonStyle.success,
                custom_id=data.to_json(),
                disabled=data.disabled))
        return self

    def add_quick_search(self, emoji: str, labels: List[Label]):
        if labels:
            for label in labels:
                self.options.append(
                    SelectOption(
                        label=label.name,
                        value=label.url,
                        description=label.amount,
                        emoji=emoji))
        return self

    def create(self):
        for i in range(0, len(self.options), 25):
            self.view.add_item(
                Select(
                    options=self.options[i:i+25],
                    placeholder="快速查詢"))
        return self.view
