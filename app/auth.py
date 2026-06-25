from ldap3 import Server, Connection, ALL, SUBTREE
from flask import current_app


def authenticate_ad(username, password):
    if not username or not password:
        return None

    ad_server = current_app.config["AD_SERVER"]
    ad_domain = current_app.config["AD_DOMAIN"]
    base_dn = current_app.config["AD_BASE_DN"]

    user_login = f"{username}@{ad_domain}"

    try:
        server = Server(ad_server, get_info=ALL)

        conn = Connection(
            server,
            user=user_login,
            password=password,
            auto_bind=True
        )

        conn.search(
            search_base=base_dn,
            search_filter=f"(sAMAccountName={username})",
            search_scope=SUBTREE,
            attributes=["memberOf", "sAMAccountName"]
        )

        if not conn.entries:
            conn.unbind()
            return None

        user_entry = conn.entries[0]

        groups = []
        if hasattr(user_entry, "memberOf"):
            groups = [str(group) for group in user_entry.memberOf]

        role = get_role_from_groups(groups)

        conn.unbind()

        if not role:
            return None

        return {
            "username": username,
            "role": role,
            "groups": groups
        }

    except Exception as error:
        print(f"LDAP authentication error: {error}")
        return None


def get_role_from_groups(groups):
    admin_group = current_app.config["AD_GROUP_ADMIN"]
    operador_group = current_app.config["AD_GROUP_OPERADOR"]
    consulta_group = current_app.config["AD_GROUP_CONSULTA"]

    for group in groups:
        if admin_group in group:
            return "admin"

        if operador_group in group:
            return "operador"

        if consulta_group in group:
            return "consulta"

    return None