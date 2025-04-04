def invalid_option(conversationHistory, msg, optionsMessage):
    conversationHistory.append("hola")
    msg.body("⚠️ *Opción no válida* ⚠️\n\n" f"{optionsMessage}")


def apply_to_offer(input, conversationHistory, msg):
    msg.body(
        "📌 *Aplicar para la oferta* 📌\n\n"
        "Dependiendo de los resultados de su evaluación, aplica para el inicial de la oferta desde RD$10 pesos en adelante.\n"
        "Para aplicar, necesita:\n"
        "1️⃣ Foto de su cédula o Pasaporte.\n"
        "2️⃣ Dos familiares que den referencias. (*Se contactarán*)\n"
        "3️⃣ Monto inicial 😎\n\n"
        "*Envíe sus documentos* para validar su proceso y nos pondremos en contacto con usted.\n\n"
        "Si quieres cancelar el proceso, envia *calcelar*"
    )
    conversationHistory.append(input)


def item_selected(conversationHistory, items, input, msg):
    itemToOffer = items[int(input) - 1]
    conversationHistory.pop()
    conversationHistory.pop()
    conversationHistory.pop()
    apply_to_offer(input, conversationHistory, msg)
