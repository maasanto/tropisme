<p>Bonjour,</p>

<p>{% set event = frappe.get_doc("Event", doc.evenement) %}</p>

<p>Un technicien vient d'apporter une réponse à la proposition de poste qui lui a été faite pour l'événement {{ event.subject }} du {{ frappe.utils.format_date(event.starts_on) }}.</p>

<p>Voici la liste des réponses apportées jusqu'ici:</p>

<ul>
{% for technicien in event.equipe_technique %}

<li>
    <strong>{{ technicien.nom_de_lemployé}}: </strong>
    <span>{{ technicien.statut }}</span>
</li>

{% endfor %}
</ul>

<p>Bonne journée !</p>
