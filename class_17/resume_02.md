# Resumen extendido y practico: VPS + OpenClaw + clave LLM de 4Geeks

Este documento resume, en orden de ejecucion real, todo lo que necesitas para dejar funcionando tu asistente AI personal con OpenClaw en una VPS.

## 1) Que necesitas antes de empezar

- Cuenta activa de estudiante en 4Geeks.
- VS Code instalado.
- Extension Remote - SSH instalada en VS Code.
- Llaves SSH generadas en tu equipo local.
- Conocimientos basicos de terminal Linux.

Si te falta base, revisa los contenidos de clase en:

- [class_17/introduction_to_vps_for_beginners.json](class_17/introduction_to_vps_for_beginners.json)
- [class_17/introduction_to_ssh_for_beginners.json](class_17/introduction_to_ssh_for_beginners.json)
- [class_17/managing_a_vps_from_vs_code.json](class_17/managing_a_vps_from_vs_code.json)
- [class_17/introduction_to_openclaw.json](class_17/introduction_to_openclaw.json)
- [class_17/setting_up_your_personal_ai_assistant.json](class_17/setting_up_your_personal_ai_assistant.json)

## 2) De donde sacar la VPS en 4Geeks

Segun el contenido de la clase:

- Entra a tu perfil de 4Geeks.
- Ve a la seccion Recursos.
- Dentro de Recursos, abre la pestaña Recursos.
- Crea una VPS seleccionando:
  - Region
  - Tipo de VPS
  - Sistema operativo

Al crearla, 4Geeks te da credenciales de acceso, tipicamente:

- IP publica
- Host
- Usuario (en muchos casos root)
- Password inicial o datos para autenticar por llave

Nota: esto aparece explicado en la unidad de VPS dentro de [class_17/introduction_to_vps_for_beginners.json](class_17/introduction_to_vps_for_beginners.json).

## 3) De donde sacar la clave LLM de 4Geeks

Segun la unidad de onboarding de OpenClaw:

- Entra a Recursos en 4Geeks.
- Genera tu API key (clave LLM) para el proveedor via LiteLLM.
- Guarda esa clave para usarla en el asistente de instalacion de OpenClaw.

Ademas, en ese mismo flujo se indica que para estudiantes de 4Geeks:

- Se usa LiteLLM como provider.
- Se puede ingresar modelo manualmente tomando el nombre del modelo desde la seccion de recursos.

Referencia: [class_17/setting_up_your_personal_ai_assistant.json](class_17/setting_up_your_personal_ai_assistant.json).

## 4) Flujo completo recomendado (orden correcto)

1. Crear VPS en 4Geeks y copiar IP publica + usuario SSH.
2. En tu computadora local, verificar acceso SSH por terminal.
3. En VS Code (local), conectarte con Remote - SSH al mismo host.
4. Ya dentro de VS Code remoto (terminal del servidor), preparar swap.
5. En VS Code remoto, instalar OpenClaw con el instalador oficial.
6. Completar onboarding de OpenClaw:
  - Aceptar disclaimer de seguridad.
  - Elegir Quick Start.
  - Elegir LiteLLM.
  - Pegar API key de 4Geeks.
  - Elegir/ingresar modelo sugerido por 4Geeks.
7. En VS Code remoto, ajustar openclaw.json para usar el endpoint de 4Geeks.
8. Reiniciar el servicio openclaw-gateway.
9. Verificar estado y abrir primer chat de prueba.

## 5) Comandos clave que debes dominar

### 5.1 Comandos que se ejecutan en LOCAL (tu laptop)

Estos comandos se ejecutan en tu terminal local (fuera del servidor):

```bash
# 1) Verifica que tienes cliente SSH
ssh -V

# 2) Conecta por SSH (reemplaza los valores)
ssh root@TU_IP_PUBLICA

# 3) Variante si necesitas una llave privada especifica
ssh -i ~/.ssh/tu_llave_privada root@TU_IP_PUBLICA
```

Opcional recomendado en local: crear alias SSH para VS Code Remote SSH.

```bash
# Crear carpeta .ssh si no existe
mkdir -p ~/.ssh

# Editar configuracion SSH local
nano ~/.ssh/config
```

Contenido sugerido de `~/.ssh/config`:

```sshconfig
Host vps-4geeks
  HostName TU_IP_PUBLICA
  User root
  IdentityFile ~/.ssh/tu_llave_privada
```

Ajustar permisos del archivo de configuracion SSH local:

```bash
chmod 600 ~/.ssh/config
```

### 5.2 Comandos que se ejecutan en VS CODE REMOTO (terminal del VPS)

Desde VS Code conectado por Remote - SSH (ya dentro del servidor):

```bash
# 1) Validaciones basicas de que estas en el servidor
whoami
hostname
pwd
```

```bash
# 2) Crear y activar swap de 2GB
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
sudo swapon --show
```

```bash
# 3) Instalar OpenClaw (usa el comando exacto que indique 4Geeks/OpenClaw)
# Ejemplo de formato, no inventes el instalador:
# curl -fsSL URL_DEL_INSTALLER_OFICIAL | bash
```

Durante onboarding selecciona: Quick Start -> LiteLLM -> API key de 4Geeks -> modelo de 4Geeks.

```bash
# 4) Editar configuracion de OpenClaw
cd ~/.openclaw
nano openclaw.json
```

En `openclaw.json`, revisar que el provider `litellm` use:

```json
"baseUrl": "https://llm.4geeks.ai/v1"
```

```bash
# 5) Reiniciar gateway y validar
systemctl --user restart openclaw-gateway.service
openclaw status
openclaw chat
```

### 5.3 Comando de VS Code (no terminal)

Esto se ejecuta en la interfaz de VS Code, no en bash:

- Command Palette -> `Remote-SSH: Connect to Host...` -> seleccionar `vps-4geeks`.

## 6) Que debes tener claro sobre seguridad

OpenClaw no es solo chat: puede ejecutar acciones reales en el servidor.

Por eso:

- No habilites herramientas innecesarias.
- No compartas tu clave privada SSH.
- No subas secretos a repositorios.
- Usa cuentas dedicadas para pruebas cuando conectes servicios externos.
- Ejecuta auditoria de seguridad despues del setup.

Punto de referencia de seguridad: [class_17/introduction_to_openclaw.json](class_17/introduction_to_openclaw.json).

## 7) Checklist de exito (si todo esta bien)

Debes poder marcar todo esto:

- Tengo VPS creada en 4Geeks.
- Me conecto por SSH sin errores.
- Me conecto por VS Code Remote SSH.
- OpenClaw instalado en la VPS.
- API key de 4Geeks cargada en onboarding.
- baseUrl configurado al endpoint de 4Geeks.
- openclaw status muestra servicio activo.
- openclaw chat responde correctamente.

## 8) Errores frecuentes y como resolverlos rapido

- No conecta por SSH:
  - Revisar IP publica, usuario, llave y firewall (puerto 22).
- VS Code Remote SSH falla:
  - Revisar archivo local `~/.ssh/config`, `IdentityFile` y permisos (`chmod 600`).
- OpenClaw no responde:
  - Reiniciar gateway y volver a ejecutar openclaw status.
- Timeout en gateway:
  - Puede ser falso positivo en algunas VPS; validar con chat real.
- Respuesta del modelo falla:
  - Revisar API key, modelo y `baseUrl` en `~/.openclaw/openclaw.json`.

## 9) Resumen corto en una frase

Tu ruta es: crear VPS en Recursos de 4Geeks, obtener API key LLM en Recursos, instalar y configurar OpenClaw con LiteLLM apuntando a https://llm.4geeks.ai/v1, y validar con openclaw status + openclaw chat.