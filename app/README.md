# Stock AD App

Aplicación web en Python/Flask para gestión de stock con autenticación, roles y futura integración con Active Directory.

## Funcionalidades

- Login y logout
- Restricción horaria de acceso
- Roles: admin, operador, consulta
- Alta de productos
- Registro de movimientos de ingreso/egreso
- Historial de movimientos
- Exportación CSV
- Persistencia con SQLite
- Preparada para integración LDAP/Active Directory

## Instalación

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt