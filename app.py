"""Expose a tiny release tracker and a minutes-to-hours API."""

import os

from flask import Flask, jsonify, request

MESSAGE = "Hello from release 1"


def create_app():
    """Build an app with deployment identity captured from its environment."""
    app = Flask(__name__)
    app.config["APP_ENV"] = os.getenv("APP_ENV", "local")
    app.config["COMMIT_SHA"] = os.getenv("RENDER_GIT_COMMIT", "local")

    @app.get("/health")
    def health():
        """Report readiness and the exact code revision running here."""
        return jsonify(
            status="ok",
            environment=app.config["APP_ENV"],
            commit=app.config["COMMIT_SHA"],
        )

    @app.get("/")
    def home():
        """Show the release message alongside its deployment identity."""
        return jsonify(
            message=MESSAGE,
            environment=app.config["APP_ENV"],
            commit=app.config["COMMIT_SHA"],
        )

    @app.get("/api/hours")
    def hours():
        """Convert an integer minute count from 0 through 1440 to hours."""
        try:
            minutes = int(request.args.get("minutes", ""))
        except ValueError:
            return jsonify(error="minutes must be an integer from 0 to 1440"), 400
        if not 0 <= minutes <= 1440:
            return jsonify(error="minutes must be an integer from 0 to 1440"), 400
        return jsonify(minutes=minutes, hours=round(minutes / 60, 2))

    return app


app = create_app()
