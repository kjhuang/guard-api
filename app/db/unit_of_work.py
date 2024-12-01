"""
unit of work
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class AsyncUnitOfWork:
    def __init__(self, session_factory: async_sessionmaker):
        """
        Initializes the Unit of Work with a session factory.
        """
        self.session_factory = session_factory
        self.session: AsyncSession | None = None

    async def __aenter__(self) -> "AsyncUnitOfWork":
        # Create a new session when entering the context
        self.session = self.session_factory()
        return self

    # async def __aexit__(self, exc_type, exc_value, traceback):
    #     # Clean up the session
    #     if self.session:
    #         if exc_type is not None:
    #             await self.session.rollback()
    #         await self.session.close()
    #         self.session = None

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            try:
                await self.commit()
            except Exception:
                await self.rollback()
                raise
        else:
            await self.rollback()

        if self.session:
            await self.session.close()

    async def commit(self):
        if self.session:
            await self.session.commit()

    async def rollback(self):
        if self.session:
            await self.session.rollback()

    # def __call__(self) -> AsyncSession:
    #     # Allow UnitOfWork to be called directly to retrieve the session
    #     if self.session is None:
    #         raise RuntimeError(
    #             "UnitOfWork session is not initialized. Use it within an 'async with' block."
    #         )
    #     return self.session

    # @asynccontextmanager
    # async def __call__(self):
    #     """
    #     Async context manager to manage the lifecycle of an AsyncSession.
    #     """
    #     # session: AsyncSession = self.session_factory()
    #     try:
    #         yield self.session
    #         await self.session.commit()  # Commit transaction on success
    #     except Exception as e:
    #         await self.session.rollback()  # Rollback transaction on failure
    #         raise e
    #     finally:
    #         await self.session.close()  # Always close the session
