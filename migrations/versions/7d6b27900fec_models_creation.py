"""Models creation

Revision ID: 7d6b27900fec
Revises: 
Create Date: 2024-04-23 22:01:26.827555

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel

from app.model.event import EventTypeEnum


# revision identifiers, used by Alembic.
revision = '7d6b27900fec'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    EventTypeEnum.create(op.get_bind(), checkfirst=True)

    op.create_table('categories',
                    sa.Column('id', sqlmodel.sql.sqltypes.GUID(),
                              nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.Column('name', sa.String(length=50), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_table('users',
                    sa.Column('id', sqlmodel.sql.sqltypes.GUID(),
                              nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.Column('first_name', sa.String(
                        length=50), nullable=True),
                    sa.Column('last_name', sa.String(
                        length=50), nullable=True),
                    sa.Column('email', sa.String(length=255), nullable=True),
                    sa.Column('password', sa.String(
                        length=255), nullable=True),
                    sa.Column('phone_no', sa.String(length=24), nullable=True),
                    sa.Column('is_active', sa.Boolean(), nullable=True),
                    sa.Column('is_admin', sa.Boolean(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    op.create_table('events',
                    sa.Column('id', sqlmodel.sql.sqltypes.GUID(),
                              nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.Column('description', sa.String(
                        length=2048), nullable=False),
                    sa.Column('date', sa.DateTime(), nullable=False),
                    sa.Column('location', sa.String(
                        length=255), nullable=False),
                    sa.Column('image', sa.String(length=2048), nullable=False),
                    sa.Column('evt_type', EventTypeEnum, nullable=False),
                    sa.Column('owner_id', sa.Uuid(), nullable=True),
                    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('eventcategory',
                    sa.Column('id', sqlmodel.sql.sqltypes.GUID(),
                              nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.Column('event_id', sa.Uuid(), nullable=False),
                    sa.Column('category_id', sa.Uuid(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['category_id'], ['categories.id'], ),
                    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
                    sa.PrimaryKeyConstraint('id', 'event_id', 'category_id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('eventcategory')
    op.drop_table('events')
    op.drop_table('users')
    op.drop_table('categories')
    EventTypeEnum.drop(op.get_bind(), checkfirst=True)

    # ### end Alembic commands ###
