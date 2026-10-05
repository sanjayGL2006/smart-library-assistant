from django.db import models
from django.conf import settings

class KnowledgeDocument(models.Model):
    filename = models.CharField(max_length=500)
    relative_path = models.TextField(unique=True)
    file_type = models.CharField(max_length=50)
    file_size = models.BigIntegerField(default=0)

    content_hash = models.CharField(
        max_length=64,
        db_index=True
    )

    subject = models.CharField(
        max_length=200,
        blank=True
    )

    topic = models.CharField(
        max_length=300,
        blank=True
    )

    chunk_count = models.PositiveIntegerField(default=0)
    indexed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    last_indexed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.filename


class KnowledgeChunk(models.Model):
    document = models.ForeignKey(
        KnowledgeDocument,
        on_delete=models.CASCADE,
        related_name="chunks"
    )

    chunk_index = models.PositiveIntegerField()
    content = models.TextField()

    page_number = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    token_count = models.PositiveIntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["document", "chunk_index"]
        constraints = [
            models.UniqueConstraint(
                fields=["document", "chunk_index"],
                name="unique_document_chunk"
            )
        ]

    def __str__(self):
        return f"{self.document.filename} - Chunk {self.chunk_index}"

class AIConversation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ai_conversations"
    )

    title = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


class AIMessage(models.Model):

    ROLE_CHOICES = [
        ("user", "User"),
        ("assistant", "Assistant"),
        ("system", "System"),
    ]

    conversation = models.ForeignKey(
        AIConversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    content = models.TextField()

    sources = models.JSONField(
        default=list,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
