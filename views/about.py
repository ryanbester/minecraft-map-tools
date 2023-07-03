import tkinter as tk
from tkinter import ttk

from controllers.about import AboutController
from views.view import View


class AboutFrame(View):
    frame: ttk.LabelFrame

    def build_view(self, parent, controller: AboutController):
        self.frame = ttk.LabelFrame(parent, text='About')
        self.frame.pack(fill='both', padx=7, pady=7, expand=True)

        text = ttk.Label(self.frame, text='A tool for downloading maps from Dynmap and JourneyMap')
        text.pack(padx=7, pady=7)

        version = ttk.Label(self.frame, text='Version 0.2.0')
        version.pack(padx=7, pady=7)

        copyright_lbl = ttk.Label(self.frame, text='Copyright (C) 2023 Ryan Bester')
        copyright_lbl.pack(padx=7, pady=7)

        github_btn = ttk.Button(self.frame, text='GitHub', command=controller.open_github_link)
        github_btn.pack(side=tk.LEFT, padx=7, pady=7, fill='x', expand=True)

        issues_btn = ttk.Button(self.frame, text='Issues', command=controller.open_issues_link)
        issues_btn.pack(side=tk.LEFT, padx=7, pady=7, fill='x', expand=True)
