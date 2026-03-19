# -*- coding: utf-8 -*-
"""
Estrategias de mensajes para A/B testing
Cada estrategia tiene un enfoque diferente para contactar lavaderos
"""

MESSAGE_STRATEGIES = [
    {
        "id": 1,
        "nombre": "AHORRO DE TIEMPO",
        "color": "#4CAF50",  # Verde
        "caso_uso": "Reservas online + Registro de walk-ins",
        "mensaje": """Hola {nombre_negocio},

¿Cuántas horas al día dedicas a coordinar citas por teléfono y organizar turnos manualmente?

Tengo una solución que automatiza completamente las reservas de tu lavadero. Tus clientes reservan online 24/7, y los que llegan directamente los registras en segundos. Tú solo recibes notificaciones de las nuevas reservas.

Imagina recuperar esas horas para enfocarte en lo que realmente importa: el servicio.

¿Te interesaría conocer cómo funciona?""",
        "recomendaciones": [
            "Envía este mensaje durante horas laborales (9am-6pm) cuando siente el dolor del trabajo manual",
            "Enfoca la conversación en TIEMPO ahorrado, no en características técnicas",
            "Pregunta: '¿Cuántas llamadas recibes al día para agendar?'",
            "Si menciona que tiene WhatsApp Business, di que esto COMPLEMENTA, no reemplaza",
            "Ideal para lavaderos medianos con flujo constante de clientes"
        ],
        "timing_videos": {
            "video_reservas": "Después de que respondan con interés. Envía con: 'Te muestro cómo tus clientes reservan en 2 minutos 👇'",
            "video_estado": "Opcional - solo si mencionan problema de llamadas preguntando por estado. Envía con: 'Y además se acabaron las llamadas de ¿en qué va mi auto?'"
        },
        "seguimiento": "Si no responde en 24h, envía: 'Hola {nombre}, ¿tuviste chance de revisar? Varios lavaderos en tu zona ya lo están usando y han recuperado más de 2 horas diarias'"
    },
    {
        "id": 2,
        "nombre": "MODERNIZACIÓN",
        "color": "#2196F3",  # Azul
        "caso_uso": "Reservas online (énfasis en presencia digital)",
        "mensaje": """Hola {nombre_negocio},

Noté que tu lavadero aparece en Google Maps. ¿Ya tienes sistema de reservas online o tus clientes aún llaman para agendar?

La competencia está modernizándose rápido. Los lavaderos con sistema online están captando más clientes jóvenes que prefieren agendar desde el celular sin tener que llamar.

Desarrollé una plataforma específica para lavaderos que les permite competir con las grandes cadenas, pero sin costos gigantes.

¿Te gustaría ver cómo se ve?""",
        "recomendaciones": [
            "Funciona mejor con lavaderos que ya tienen presencia digital (Google Maps, redes sociales)",
            "Envía en horarios de tarde (2pm-5pm) cuando hay menos movimiento para pensar estratégicamente",
            "Si tienen Instagram o Facebook activo, menciona que viste su perfil",
            "Enfatiza que esto los pone al nivel de cadenas grandes pero sin la inversión",
            "Ideal para lavaderos en zonas competitivas o cercanos a universidades"
        ],
        "timing_videos": {
            "video_reservas": "En el PRIMER mensaje o inmediatamente después. Envía con: 'Acá te dejo un video de cómo luce una experiencia de reserva moderna 🚀'",
            "video_estado": "Después si responde positivamente. Envía con: 'Y mira esto - tus clientes pueden trackear su auto como si fuera un delivery de Rappi'"
        },
        "seguimiento": "Si no responde en 48h, envía: 'Hola {nombre}, vi que [menciona algo específico de su Google Maps/redes]. ¿Revisaste la plataforma? Podría ayudarte a destacar aún más'"
    },
    {
        "id": 3,
        "nombre": "SATISFACCIÓN DEL CLIENTE",
        "color": "#FF9800",  # Naranja
        "caso_uso": "Registro de walk-ins + Tracking en tiempo real",
        "mensaje": """Hola {nombre_negocio},

¿Tus clientes te preguntan constantemente "en qué va mi auto"?

Imagina que en lugar de estar respondiendo llamadas todo el día, tus clientes reciban notificaciones automáticas: cuando empiezas el lavado, cuando está en proceso, y cuando está listo para retirar.

El resultado: clientes felices que sienten que tienen control, y tú sin interrupciones constantes.

Así funcionan los lavaderos premium, y ahora está al alcance de cualquier lavadero.

¿Quieres ver cómo funciona?""",
        "recomendaciones": [
            "Ideal para lavaderos con alto volumen de clientes y muchas consultas",
            "Envía en horarios de máxima ocupación (sábados/domingos 10am-2pm) cuando sienten el dolor",
            "Enfatiza las notificaciones automáticas por WhatsApp - es el diferenciador clave",
            "Pregunta: '¿Cuántas veces al día te preguntan por el estado del auto?'",
            "Perfecto para lavaderos que ya están saturados y necesitan eficiencia"
        ],
        "timing_videos": {
            "video_reservas": "OPCIONAL - solo si también quieren captar más clientes. Menciona: 'Ah, y también pueden agendar online si quieres'",
            "video_estado": "PRINCIPAL - Después de confirmar que es un problema que tiene. Envía con: 'Mira cómo tus clientes ven el estado de su auto en tiempo real 📱'"
        },
        "seguimiento": "Si no responde, envía: '¿Te pasa seguido que los clientes llaman cada 20 minutos preguntando si ya está listo?'"
    },
    {
        "id": 4,
        "nombre": "AUMENTO DE INGRESOS",
        "color": "#9C27B0",  # Púrpura
        "caso_uso": "Reservas online 24/7",
        "mensaje": """Hola {nombre_negocio},

Pregunta rápida: ¿Cuántos clientes pierdes porque llaman cuando estás ocupado y no contestas?

Los lavaderos que usan sistema de reservas online están viendo entre 20-30% más citas porque captan clientes 24/7, incluso cuando están cerrados o muy ocupados.

La plataforma les permite:
✅ Recibir reservas a las 11pm de clientes que planean su semana
✅ Vender paquetes premium y extras antes de que llegue el cliente
✅ Llenar los huecos muertos del día automáticamente

¿Te gustaría ver los números reales?""",
        "recomendaciones": [
            "Para dueños enfocados en crecimiento y resultados económicos",
            "Mejor momento: Lunes en la mañana (9-11am) cuando planean la semana",
            "Enfatiza ROI, recuperación de inversión rápida y aumento de facturación",
            "Menciona casos de éxito si los tienes (incluso de forma genérica: 'otros lavaderos')",
            "Pregunta sobre cuántos clientes cree que pierde por semana"
        ],
        "timing_videos": {
            "video_reservas": "Junto con el primer mensaje - el visual de reservas vende por sí solo. Envía con: 'Mira las reservas que podrías estar recibiendo a cualquier hora 💰'",
            "video_estado": "Secundario - mencionar como valor agregado. 'Y de paso, tus clientes ven el estado sin llamarte'"
        },
        "seguimiento": "Si no responde: '¿Cuántas citas calculas que pierdes por semana por no tener disponibilidad de agendar online? Incluso recuperando 3-4 semanales ya se paga solo'"
    },
    {
        "id": 5,
        "nombre": "ORGANIZACIÓN/CONTROL",
        "color": "#F44336",  # Rojo
        "caso_uso": "Registro de walk-ins + Panel de administración",
        "mensaje": """Hola {nombre_negocio},

¿Usas cuaderno, Excel o WhatsApp para llevar control de tus citas?

Déjame adivinar: a veces hay doble agendamiento, clientes que dicen que agendaron y no están en el registro, o confusión con quién pidió qué paquete.

Tengo una plataforma que te da control total:
✅ Panel donde ves todas las citas del día en un solo lugar
✅ Registro automático de cada cliente que llega
✅ Historial completo de servicios y preferencias de cada cliente
✅ Reportes de ingresos y servicios más vendidos

Es como pasar de cuaderno a tener un sistema profesional.

¿Te interesa?""",
        "recomendaciones": [
            "Para lavaderos tradicionales que se ven desorganizados o sin tecnología",
            "Envía los lunes (después del caos del fin de semana) o martes temprano",
            "Enfatiza la facilidad de uso - 'no necesitas ser experto en tecnología'",
            "Pregunta qué método usan actualmente para llevar control",
            "Si mencionan Excel o cuaderno, enfatiza: 'Esto es tan fácil como el cuaderno pero sin los errores'"
        ],
        "timing_videos": {
            "video_reservas": "OPCIONAL - solo si muestran interés en crecer. 'Ah, y si quieres también pueden agendar online'",
            "video_estado": "NO prioritario - enfocarse en el panel de administración. Solo mencionar si preguntan por más funciones"
        },
        "seguimiento": "Si no responde: '¿Cómo llevas el control de tus citas actualmente? ¿Te ha pasado que hayan confusiones o dobles agendamientos?'"
    },
    {
        "id": 6,
        "nombre": "SOLUCIÓN A PROBLEMA ESPECÍFICO",
        "color": "#00BCD4",  # Cyan
        "caso_uso": "Reservas online + Registro walk-ins",
        "mensaje": """Hola {nombre_negocio},

Vi tu lavadero en Google Maps y me di cuenta de algo: probablemente pierdes clientes porque no saben cuánto tiempo tienen que esperar o si tienes disponibilidad.

Hice una plataforma específica para lavaderos donde:
✅ Los clientes ven horarios disponibles en tiempo real
✅ Seleccionan el paquete antes de llegar (y tú ya sabes qué esperar)
✅ Optimizas tu agenda sin espacios vacíos ni sobrecarga

El resultado: tu lavadero siempre lleno, clientes que llegan sabiendo exactamente qué van a pagar y cuándo van a entrar.

¿Quieres que te muestre cómo se ve desde el lado del cliente?""",
        "recomendaciones": [
            "Para lavaderos con problemas visibles de gestión de espera o filas",
            "Envía en horarios pico cuando sienten el problema (sábado 11am-1pm)",
            "Personaliza mencionando algo que viste en su perfil de Google Maps",
            "Si tienen reseñas sobre tiempos de espera, menciónalo sutilmente",
            "Ideal para lavaderos en zonas muy transitadas o con mucha competencia"
        ],
        "timing_videos": {
            "video_reservas": "En el SEGUNDO mensaje - primero genera interés. Envía con: 'Mira cómo tus clientes eligen su horario sin tener que llamar 📅'",
            "video_estado": "Si hay interés después del primero. Envía con: 'Y pueden ver cuándo estará listo su auto, como un rastreo de paquete'"
        },
        "seguimiento": "Si no responde: '¿Qué días sueles tener más movimiento? Te muestro cómo optimizar esos días para que no se te escape ni un cliente'"
    }
]


def get_message_for_business(business_index: int) -> dict:
    """
    Asigna un mensaje a un negocio basado en su índice
    Distribuye ~10 negocios por estrategia de forma cíclica

    Args:
        business_index: Índice del negocio en la lista (0-based)

    Returns:
        Diccionario con la estrategia de mensaje asignada
    """
    # Cada 10 negocios cambiamos de estrategia
    # Negocio 0-9 -> Mensaje 1
    # Negocio 10-19 -> Mensaje 2, etc.
    strategy_index = (business_index // 10) % len(MESSAGE_STRATEGIES)
    return MESSAGE_STRATEGIES[strategy_index].copy()


def personalize_message(strategy: dict, business_name: str) -> dict:
    """
    Personaliza el mensaje con el nombre del negocio

    Args:
        strategy: Diccionario con la estrategia
        business_name: Nombre del negocio

    Returns:
        Diccionario con mensaje y seguimiento personalizados
    """
    personalized = strategy.copy()

    # Personalizar mensaje principal
    personalized['mensaje_personalizado'] = strategy['mensaje'].replace(
        '{nombre_negocio}',
        business_name if business_name and business_name != 'N/A' else ''
    ).strip()

    # Personalizar mensaje de seguimiento (solo primer nombre)
    primer_nombre = business_name.split()[0] if business_name and business_name != 'N/A' else business_name
    personalized['seguimiento_personalizado'] = strategy['seguimiento'].replace(
        '{nombre}',
        primer_nombre if primer_nombre else ''
    ).strip()

    return personalized
