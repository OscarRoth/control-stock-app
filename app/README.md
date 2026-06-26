# Stock AD App

Aplicación web desarrollada con **Python** y **Flask** para la gestión de stock de repuestos, integrada con **Active Directory** mediante LDAP para la autenticación de usuarios, administración de roles y control de acceso.

## Características

* Autenticación mediante Active Directory (LDAP).
* Inicio y cierre de sesión.
* Control de acceso basado en roles.
* Restricción horaria de acceso administrada desde Active Directory.
* Gestión de productos.
* Registro de movimientos de ingreso y egreso de stock.
* Historial de movimientos.
* Exportación de datos a CSV.
* Panel de control con indicadores de inventario.
* Interfaz moderna desarrollada con Tailwind CSS.
* Persistencia de datos mediante SQLite.

## Roles del sistema

### Administrador

* Gestiona productos.
* Registra movimientos.
* Administra usuarios y permisos.
* Accede a todas las funcionalidades del sistema.

### Operador

* Consulta el inventario.
* Registra ingresos y egresos de stock.
* No posee permisos administrativos.

### Consulta

* Visualiza productos, stock e historial.
* No puede modificar información.

## Tecnologías utilizadas

* Python 3
* Flask
* SQLAlchemy
* SQLite
* LDAP3
* Active Directory
* HTML5
* Tailwind CSS
* Jinja2
* Git y GitHub

## Requisitos

* Python 3.11 o superior
* Windows Server con Active Directory
* Servidor LDAP habilitado
* Entorno virtual (venv)

## Instalación

```bash
python -m venv venv
```

Activar el entorno virtual:

**Windows**

```bash
venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Variables de entorno

Crear un archivo `.env` con la siguiente configuración:

```env
SECRET_KEY=change-me
DATABASE_URL=sqlite:///stock.db

LOGIN_START_HOUR=8
LOGIN_END_HOUR=18

DEV_LOGIN=false

AD_SERVER=ldap://192.168.0.198
AD_DOMAIN=IFTS.LOCAL
AD_BASE_DN=DC=IFTS,DC=LOCAL

AD_GROUP_ADMIN=GG_Stock_Admin
AD_GROUP_OPERADOR=GG_Stock_Operador
AD_GROUP_CONSULTA=GG_Stock_Consulta
```

## Integración con Active Directory

La autenticación se realiza mediante LDAP utilizando usuarios del dominio.

Los permisos se asignan según la pertenencia a los siguientes grupos:

* **GG_Stock_Admin**
* **GG_Stock_Operador**
* **GG_Stock_Consulta**

La restricción horaria de acceso se administra desde **Active Directory** mediante la configuración **Logon Hours** de cada usuario.

## Estructura del proyecto

```
stock-ad-app/
│
├── app/
│   ├── auth.py
│   ├── models.py
│   ├── routes.py
│   ├── forms.py
│   ├── templates/
│   ├── static/
│   └── ...
│
├── migrations/
├── instance/
├── requirements.txt
├── run.py
└── README.md
```

## Autor

Proyecto desarrollado como trabajo académico para la integración de aplicaciones Python/Flask con Active Directory, implementando autenticación LDAP, control de acceso basado en roles y administración centralizada de usuarios.
