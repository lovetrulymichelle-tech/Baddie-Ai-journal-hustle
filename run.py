#!/usr/bin/env python3
"""Run the Baddie AI Journal application."""

from baddie_journal.app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)