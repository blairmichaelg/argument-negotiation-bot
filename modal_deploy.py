import modal

app = modal.App("argument-negotiation-bot")


@app.function(
    image=modal.Image.debian_slim().pip_install(
        "fastapi",
        "uvicorn",
        "openai",
        "sqlalchemy",
        "pydantic",
        "requests",
        "cachetools",
    )
)
def run():
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    with app.run():
        run.call()
