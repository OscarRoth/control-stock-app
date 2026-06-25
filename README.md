# Sistema de Control de Stock con Active Directory

Aplicación web desarrollada en Python/Flask para la gestión de stock de piezas y repuestos para camiones y vehículos pesados, inspirada en el modelo operativo de Don Telmo, empresa dedicada a la venta y distribución de repuestos y accesorios para transporte pesado.

## Objetivo del proyecto

El objetivo es implementar un sistema interno de control de inventario que permita:

* Administrar productos.
* Registrar ingresos y egresos de stock.
* Consultar historial de movimientos.
* Exportar información en formato CSV.
* Autenticar usuarios contra Active Directory.
* Asignar permisos según grupos del dominio.
* Restringir el acceso por horario.

## Contexto aplicado

El sistema está pensado para una empresa de repuestos para camiones, buses y maquinaria pesada. El inventario puede incluir categorías como:

* Frenos.
* Llantas.
* Amortiguadores de chasis.
* Lámparas.
* Suspensión neumática.
* Electricidad.
* Tubos de poliamida.
* Filtros.
* Hélices y viscosas.
* Lubricantes.
* Válvulas.
* Repuestos varios.
* Accesorios.

## Tecnologías utilizadas

* Python
* Flask
* Flask-Login
* Flask-SQLAlchemy
* SQLite
* LDAP3
* Active Directory
* Windows Server 2008 R2
* Git / GitHub

## Funcionalidades principales

### Productos

Permite registrar productos con:

* SKU
* Nombre
* Stock inicial

También valida:

* Que el stock no sea negativo.
* Que no se repita el SKU.

### Movimientos de stock

Permite registrar:

* Ingresos
* Egresos

El sistema actualiza automáticamente el stock disponible.

También valida:

* Que la cantidad sea mayor a cero.
* Que el producto exista.
* Que no se pueda egresar más stock del disponible.

### Historial

Permite consultar los movimientos realizados, indicando:

* Producto
* Tipo de movimiento
* Cantidad
* Usuario
* Fecha

### Exportación CSV

Permite exportar el listado de productos en formato `.csv`.

## Integración con Active Directory

La aplicación autentica usuarios contra un dominio Active Directory mediante LDAP.

Dominio utilizado en laboratorio:

```text
IFTS.LOCAL
```

OU utilizada para la aplicación:

```text
GCBA
└── Aplicaciones
    └── StockApp
```

Usuarios de prueba:

```text
stock.admin
stock.operador
stock.consulta
```

Grupos de seguridad:

```text
GG_Stock_Admin
GG_Stock_Operador
GG_Stock_Consulta
```

## Roles y permisos

| Grupo de Active Directory | Rol en la aplicación | Permisos                                |
| ------------------------- | -------------------- | --------------------------------------- |
| GG_Stock_Admin            | admin                | Acceso completo                         |
| GG_Stock_Operador         | operador             | Ver productos y registrar movimientos   |
| GG_Stock_Consulta         | consulta             | Ver productos, historial y exportar CSV |

## Restricción horaria

La aplicación permite restringir el acceso según horario.

Ejemplo configurado:

```text
LOGIN_START_HOUR=8
LOGIN_END_HOUR=18
```

Durante las pruebas se puede modificar temporalmente a:

```text
LOGIN_START_HOUR=0
LOGIN_END_HOUR=24
```

## Variables de entorno

El archivo `.env` debe contener:

```env
SECRET_KEY=change-me
DATABASE_URL=sqlite:///stock.db

LOGIN_START_HOUR=8
LOGIN_END_HOUR=18

DEV_LOGIN=false

AD_SERVER=ldap://IP_DEL_CONTROLADOR_DE_DOMINIO
AD_DOMAIN=IFTS.LOCAL
AD_BASE_DN=DC=IFTS,DC=LOCAL

AD_GROUP_ADMIN=GG_Stock_Admin
AD_GROUP_OPERADOR=GG_Stock_Operador
AD_GROUP_CONSULTA=GG_Stock_Consulta
```

Ejemplo usado en laboratorio:

```env
AD_SERVER=ldap://192.168.0.219
```

## Instalación del proyecto

Clonar el repositorio:

```bash
git clone https://github.com/OscarRoth/control-stock-app.git
cd control-stock-app
```

Crear entorno virtual:

```bash
python -m venv venv
```

Activar entorno virtual en Windows:

```powershell
.\venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar la aplicación:

```bash
python run.py
```

Abrir en el navegador:

```text
http://127.0.0.1:5000
```

## Estructura general del proyecto

```text
stock-ad-app
├── app
│   ├── templates
│   ├── __init__.py
│   ├── auth.py
│   ├── config.py
│   ├── models.py
│   ├── permissions.py
│   └── routes.py
├── instance
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

## Seguridad aplicada

El proyecto implementa:

* Autenticación LDAP contra Active Directory.
* Separación de permisos por rol.
* Restricción horaria de acceso.
* Protección de rutas mediante login requerido.
* Protección de rutas según rol.
* Variables sensibles fuera del repositorio mediante `.env`.
* Exclusión de `.env`, base local y entorno virtual mediante `.gitignore`.

## Infraestructura Active Directory

Se creó la siguiente estructura:

```text
IFTS.LOCAL
└── GCBA
    ├── Aplicaciones
    │   └── StockApp
    ├── Gerencia
    ├── RecursosHumanos
    └── SoporteTecnico
```

Además, se configuraron:

* Usuarios por departamento.
* Grupos globales de seguridad.
* Usuarios asociados a sus grupos.
* Políticas de grupo.
* Restricción horaria.
* Bloqueo de CMD y Regedit.
* Bloqueo de dispositivos USB.
* Restricción de configuración de red.
* Mensaje de advertencia al iniciar sesión.

## Estado del proyecto

Proyecto funcional para entorno académico/laboratorio.

No está preparado para producción sin ajustes adicionales, como:

* Base de datos productiva.
* HTTPS.
* Manejo avanzado de errores.
* Auditoría persistente.
* Logs centralizados.
* Despliegue en servidor WSGI.
* Hardening de Active Directory.
