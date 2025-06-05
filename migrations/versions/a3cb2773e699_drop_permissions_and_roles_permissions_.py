"""drop permissions and roles_permissions tables and delete relation in role model

Revision ID: a3cb2773e699
Revises: d3af567215ee
Create Date: 2025-06-04 07:27:25.503190

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = 'a3cb2773e699'
down_revision = 'd3af567215ee'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)

    if 'roles_permissions' in inspector.get_table_names():
        op.drop_table('roles_permissions')

    if 'permissions' in inspector.get_table_names():
        op.drop_table('permissions')


def downgrade():
    # 1. Buat ulang tabel permissions lebih dulu (karena roles_permissions tergantung padanya)
    op.create_table(
        'permissions',
        sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('name', mysql.VARCHAR(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        mysql_engine='InnoDB',
        mysql_default_charset='utf8mb4',
        mysql_collate='utf8mb4_0900_ai_ci'
    )

    # Tambahkan kembali index unik pada kolom name
    with op.batch_alter_table('permissions', schema=None) as batch_op:
        batch_op.create_index('ix_permissions_name', ['name'], unique=True)

    # 2. Buat ulang tabel roles_permissions setelah permissions tersedia
    op.create_table(
        'roles_permissions',
        sa.Column('role_id', mysql.INTEGER(), nullable=False),
        sa.Column('permission_id', mysql.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name='roles_permissions_ibfk_2'),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], name='roles_permissions_ibfk_1'),
        mysql_engine='InnoDB',
        mysql_default_charset='utf8mb4',
        mysql_collate='utf8mb4_0900_ai_ci'
    )
