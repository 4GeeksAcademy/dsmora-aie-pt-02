# Guia Docente Completa: Class 17 - VPS, SSH, VS Code remoto y Asistente AI personal

Clase online para 90 minutos.
Version enfocada en practica real, seguridad basica y configuracion guiada paso a paso.

## 1) Objetivos de aprendizaje

Al finalizar, el estudiante podra:

- Explicar que es un VPS y cuando conviene usarlo.
- Conectarse por SSH de forma segura (llave publica/privada).
- Configurar y usar Remote SSH en VS Code para trabajar sobre el servidor.
- Reconocer riesgos de seguridad comunes y aplicar medidas minimas.
- Instalar y validar OpenClaw en un VPS.
- Configurar un asistente AI personal y ejecutar un primer flujo de prueba.

## 2) Mapa de clase y tiempo sugerido (90 min)

- Apertura y objetivos: 5 min
- Bloque A - Fundamentos de VPS: 12 min
- Bloque B - SSH desde cero: 18 min
- Bloque C - VS Code remoto y flujo de trabajo: 15 min
- Bloque D - Seguridad practica para laboratorio: 12 min
- Bloque E - Introduccion a OpenClaw: 10 min
- Bloque F - Setup del asistente AI personal: 13 min
- Cierre, checklist y siguientes pasos: 5 min

## 3) Guion docente detallado

## Apertura (5 min)

Mensaje sugerido:

"Hoy vamos a pasar de teoria a operacion real: servidor en la nube, acceso seguro, trabajo remoto desde VS Code y asistente AI funcionando en tu propia infraestructura."

Preparacion del docente:

- Tener un VPS de demo accesible.
- Tener una terminal local y una terminal remota abiertas.
- Tener VS Code con extension Remote SSH lista.
- Tener una cuenta de demo para mostrar instalacion/configuracion de OpenClaw.

## Bloque A - Fundamentos de VPS (12 min)

Conceptos clave:

- Un VPS es una maquina virtual siempre encendida en la nube.
- Diferencia entre entorno local y entorno remoto.
- Recursos base: CPU, RAM, disco, red.
- Casos de uso: APIs, bots, automatizaciones, assistants self-hosted.

### Demo A1 - Reconocer el servidor

```bash
uname -a
cat /etc/os-release
uptime
free -h
df -h
```

Puntos para explicar:

- El servidor tiene estado propio e independiente del equipo local.
- Hay que vigilar recursos para estabilidad.

### Mini debate guiado

Preguntas rapidas:

- Que correria en local y que correria en VPS?
- Que pasa si el servidor se queda sin disco?

## Bloque B - SSH desde cero (18 min)

Conceptos clave:

- SSH cifra la comunicacion cliente-servidor.
- Recomendado: autenticacion por llaves, no por password.
- Flujo: generar llave, registrar llave publica, conectar.

### Demo B1 - Generar y revisar llaves

```bash
ssh-keygen -t ed25519 -C "student@example.com"
ls -la ~/.ssh
cat ~/.ssh/id_ed25519.pub
```

### Demo B2 - Primera conexion

```bash
ssh user@IP_DEL_VPS
```

### Demo B3 - Configuracion de alias SSH

```bash
cat >> ~/.ssh/config <<'EOF'
Host mi-vps
  HostName IP_DEL_VPS
  User user
  IdentityFile ~/.ssh/id_ed25519
EOF

chmod 600 ~/.ssh/config
ssh mi-vps
```

Errores comunes a cubrir:

- Permisos incorrectos en `~/.ssh`.
- IP, usuario o llave equivocada.
- Bloqueo por firewall o puerto SSH cerrado.

## Bloque C - VS Code remoto y flujo de trabajo (15 min)

Conceptos clave:

- VS Code local, archivos/procesos ejecutandose en remoto.
- Ventaja: mismo editor, pero entorno real del servidor.
- Validacion en terminal integrada remota.

### Demo C1 - Abrir host remoto

Pasos:

- Abrir paleta de comandos.
- Ejecutar `Remote-SSH: Connect to Host...`.
- Elegir `mi-vps`.
- Abrir carpeta de trabajo del servidor.

### Demo C2 - Verificacion de contexto remoto

```bash
pwd
hostname
whoami
```

### Actividad guiada

- Crear un archivo de prueba en remoto.
- Editarlo desde VS Code.
- Ejecutarlo por terminal remota.

## Bloque D - Seguridad practica para laboratorio (12 min)

Conceptos clave:

- Principio de minimo privilegio.
- Secretos fuera de repositorios.
- Hardening basico inicial.

### Demo D1 - Actualizacion y firewall basico

```bash
sudo apt update && sudo apt upgrade -y
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status
```

### Demo D2 - Buenas practicas de secretos

```bash
echo "API_KEY=coloca_aqui_tu_valor" > .env
echo ".env" >> .gitignore
```

Riesgos a remarcar (del contenido OpenClaw):

- Exponer puertos sin control.
- Compartir llaves privadas.
- Dejar servicios sin autenticacion.

## Bloque E - Introduccion a OpenClaw (10 min)

Conceptos clave:

- Que es OpenClaw y que resuelve.
- Arquitectura basica: runtime, configuracion y archivos de contexto.
- Rol del servidor para tener un asistente disponible 24/7.

### Demo E1 - Instalacion conceptual guiada

Secuencia sugerida:

- Validar dependencias base.
- Instalar OpenClaw segun su guia.
- Verificar que responde a comandos iniciales.

Actividad rapida:

- Pedir a estudiantes explicar con sus palabras el flujo de "prompt -> proceso -> respuesta".

## Bloque F - Setup del asistente AI personal (13 min)

Conceptos clave:

- Conexion al VPS.
- Instalacion de OpenClaw.
- Configuracion inicial (`openclaw.json` o archivo equivalente).
- Primera conversacion de prueba.

### Demo F1 - Checklist de instalacion

Checklist docente:

- Conexion SSH activa al VPS.
- OpenClaw instalado.
- Archivo de configuracion editado.
- Variables de entorno cargadas.
- Proceso levantado sin errores.

### Demo F2 - Primera prueba funcional

Objetivo:

- Ejecutar una consulta simple al asistente.
- Confirmar salida esperada.
- Revisar logs basicos para diagnostico.

### Ejercicio final (individual o parejas)

Consigna:

- Cada estudiante debe completar un "smoke test":
  - Conectar al VPS por SSH.
  - Abrir el host en VS Code remoto.
  - Validar que el asistente responde una instruccion simple.

Criterios de exito:

- Conexion remota funcional.
- Configuracion minima correcta.
- Respuesta del asistente sin error fatal.

## 4) Preguntas de chequeo (durante la clase)

- Cual es la diferencia entre ejecutar algo local vs remoto?
- Por que es mas seguro usar llave SSH que password?
- Que problema resuelve VS Code Remote SSH?
- Que riesgo hay si subimos `.env` al repositorio?
- Que validas primero si el asistente no responde?

## 5) Rubrica rapida de evaluacion

- Nivel alto:
  - Conecta por SSH con llave sin ayuda.
  - Usa VS Code remoto de forma fluida.
  - Completa setup del asistente y ejecuta prueba.
  - Identifica y corrige al menos un riesgo de seguridad.

- Nivel medio:
  - Logra conexion y flujo remoto con poca ayuda.
  - Completa setup parcial del asistente.
  - Entiende riesgos, pero necesita guia para mitigarlos.

- Nivel inicial:
  - Requiere apoyo en SSH y configuracion.
  - Aun no completa prueba funcional de extremo a extremo.

## 6) Cierre (5 min)

Resumen sugerido:

"Hoy armamos la base operativa profesional: servidor en la nube, canal seguro de acceso, entorno remoto productivo y asistente AI personal corriendo en infraestructura propia."

Tarea sugerida:

- Documentar en markdown su flujo final (SSH + VS Code remoto + OpenClaw).
- Agregar una seccion de troubleshooting con 3 errores reales y su solucion.
- Preparar el entorno para la siguiente clase (automatizacion o despliegue continuo).