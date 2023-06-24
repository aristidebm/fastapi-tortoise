from aerich import Command


async def migrate(app, config):
    """
    Create all tables
    """
    command = Command(app=app, tortoise_config=config)
    await command.upgrade()


async def rollback(app, config):
    """
    Drop all tables
    """
    command = Command(app=app, tortoise_config=config)
    await command.downgrade()
