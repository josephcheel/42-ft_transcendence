# Transcendence

Todas las interacciones entre contenedores se deberan de hacer por json. Si un contenedor debe de pasar informacion de uno a otro debera de enviar un paquete json con la informacion correspondiente. Cada contenedor debera de dar sus respuestas con paquetes en formato json. 

A excepcion de cuando se hace make, todos los contenedores deberan de funcionar sin importar el estado de los demas contenedores, por lo que cualquier interaccion entre componentes debera de estar protegida, ya sea con try/except o simplemente verificar los valores de retorno, y en caso de fallo retonar una respuesta de error apropiada, podemos dar uso de logs aqui, indicado mas informacion para luego poder examinarlos.

De momento solo monta los contenedores, cada contenedor sera una App Django o ELK/Prometheus/Grafana (stack de monitoreo)

Al hacer make monta todo los contenedores.

Estan abiertos los puertos 8000 (gateway, el unico punto de entrada)
3000 (grafana, para visualizacion con prometheus (alertas y graficas)) y 5601 (kibana, para ver logs, graficos con elasticsearch y logistash).

Los modulos de devops (ELK, Prometheus, Grafana) hacen uso del contenedor setup para crear credenciales y hacer llamadas a las APIs de cada uno de ellos para subir alertas, dashboards, puntos de contacto, y demas configuraciones, de esta forma al entrar ya se deberan de ver dashboards y demas, y luego el setup se apaga.

Kibana: usuario: elastic , contrasena: changeme

Grafana: usuario: admin , contrasena: newadmin 

## Modulo de DB:

Esta en inicio, solo usermanagement se conecta al contenedor de base de datos. 

Se debe de modificar el archivo settings.py de cada servicio y agregar:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', 5432),
    }
}

esto es lo que hace que se conecte a la base de datos. Cualquier interaccion que realice la app con la base de datos (por ejemplo:
user = User.objects.create(name=name, password=password)) django las hace automaticamente a la base de datos en el contenedor DB_HOST.

Por lo tanto, cada accion que toque la base de datos debe de estar protegida con un try: except: ya que si por algun motivo el contenedor no esta activo debera de retornar un mensaje de error.



Cada contenedor debera de correr python manage.py makemigrations && python manage.py migrate para crear los valores en la base de datos.

Actualmente usermanagement no lo hace, se debe de entrar en el contenedor y correrlo manualmente, necesitan verificar que el contenedor de la base de datos este disponible.  


## Modulo logs:

El modulo logs usa logstash para controlar archivos logs. Django automaticamente escribe al archivo configurado (mas adelante indico como modificarlo) al realizar ciertas acciones, especialmente si en settings.py DEBUG=true, escribira varios mensajes de debug

Los contenedores que tenemos ahora estan todos configurados y deberia de funcionar correctamente los logs, en la seccion Discover de Kibana se podran ver 2 dashboards con informacion de codigos que estamos retornando y los niveles de debug messages del contenedor gateway (aun no configuro otros dashboards pero ya los contendores dan la informacion)

### Escribir nuestros propios logs


import logging
logger = logging.getLogger('django')
logger.setLevel(logging.DEBUG)

se debe de colocar esto al inicio del archivo para configurar el logger. 

ahora se puede usar el logger como:

logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')

### Configurar el archivo logs

En caso de querer configurar una nueva app para que de logstash consuma los logs.

En settings.py 

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': jsonlogger.JsonFormatter,
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': f'/var/log/{LOG_FILE}',
            'formatter': 'json',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

logging.config.dictConfig(LOGGING)

se puede copiar y pegar esto en settings, lo unico que se debe de cambiar el la variable LOG_FILE

Ejemplo en usermanagement:

LOG_FILE= os.environ.get("USER_LOG", "usermanagement.log"), que use la variable USER_LOG o usermanagement.log si no encuentra la variable

en el archivo .env se encuentran los nombres de cada archivo log para los contenedores que tenemos

GATEWAY_LOG=gateway.log
USER_LOG=usermanagement.log
CHAT_LOG=chat.log
GAMESTATS_LOG=gamestats.log
TWOFACTOR_LOG=twofactor.log

importante hacerlo por variables ya que en ELK/logstash/logstash.conf se configuran los archivos que controlara logstash

Para agregar un nuevo archivo solo se debe de agregar esto al .conf en el bloque input{} 

  file {
    path => "/var/log/${NUEVO_LOG}"
    start_position => "beginning"
    sincedb_path => "/dev/null"
    tags => ["nuevo"]
  }

y luego en el bloque if/else dentro del bloque output{} del mismo archivo. Index puede ser modificado para otro nombre, pero es el que usan todos de momento.

else if "nuevo" in [tags] {
    elasticsearch {
      index => "nuevo-logs-%{+YYYY.MM.dd}"
      hosts => ["${ELASTIC_HOSTS}"]
      user => "${ELASTIC_USER}"
      password => "${ELASTIC_PASSWORD}"
      cacert => "certs/ca/ca.crt"
    }
  } 

### Algunos enlaces que use para configurar 

[ELK getting started](https://www.elastic.co/blog/getting-started-with-the-elastic-stack-and-docker-compose/)
[Kibana API](https://www.elastic.co/guide/en/kibana/current/saved-objects-api.html)
[Elastic Index Policy](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-management.html)

[Prometheus Django](https://github.com/korfuri/django-prometheus)
[Prometheus docker](https://docs.docker.com/config/daemon/prometheus/)
[Prometheus your own metrics](https://www.monterail.com/blog/prometheus-custom-metrics)

[Grafana Provisions](https://grafana.com/docs/grafana/latest/administration/provisioning/)
[Grafana contact points and rules](https://grafana.com/docs/grafana/latest/developers/http_api/alerting_provisioning/)


True
[Django User Model](https://docs.djangoproject.com/en/5.0/topics/auth/customizing/)
