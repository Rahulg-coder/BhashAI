# Android Tablet Architecture & Room Offline Database Specification

## Target Device Specifications
- **Operating System**: Android 9.0 (API Level 28) and above.
- **Hardware Profile**: Low-cost school tablet with 2 GB RAM, 16-32 GB storage.
- **UI Framework**: Jetpack Compose + Material 3.
- **Local Persistence**: Android Room Persistence Library + SQLite.

---

## Room Database Entities

```kotlin
// 1. FLN Learning Outcome Entity
@Entity(tableName = "fln_outcomes")
data class FlnOutcomeEntity(
    @PrimaryKey val outcomeId: String,
    val grade: Int,
    val subject: String,
    val domain: String,
    val competencyCode: String,
    val competency: String,
    val code: String,
    val description: String,
    val hindiDescription: String,
    val concept: String
)

// 2. Lesson Plan Entity
@Entity(
    tableName = "lessons",
    foreignKeys = [
        ForeignKey(
            entity = FlnOutcomeEntity::class,
            parentColumns = ["outcomeId"],
            childColumns = ["flnOutcomeId"],
            onDelete = ForeignKey.CASCADE
        )
    ]
)
data class LessonEntity(
    @PrimaryKey val lessonId: String,
    val flnOutcomeId: String,
    val grade: Int,
    val subject: String,
    val domain: String,
    val titleHindi: String,
    val titleSanthali: String,
    val concept: String,
    val lessonPayloadJson: String // Full serialized JSON containing intro, teacher script, activities
)

// 3. Approved Educational Glossary Entity
@Entity(tableName = "educational_glossary")
data class GlossaryTermEntity(
    @PrimaryKey val hindiTerm: String,
    val domain: String,
    val grade: Int,
    val santhaliOlChiki: String,
    val santhaliPhonetic: String,
    val mundariText: String,
    val hoText: String,
    val approved: Boolean
)

// 4. Local Content Sync Metadata Entity
@Entity(tableName = "sync_metadata")
data class SyncMetadataEntity(
    @PrimaryKey val id: Int = 1,
    val localContentVersion: Int,
    val lastSyncTimestamp: Long
)
```

---

## Incremental Sync Flow

```kotlin
class ContentSyncRepository(
    private val apiService: BhashAIApiService,
    private val db: BhashAIRoomDatabase
) {
    suspend fun syncContent(): Result<Boolean> = withContext(Dispatchers.IO) {
        val currentVersion = db.syncDao().getMetadata()?.localContentVersion ?: 0
        try {
            val response = apiService.getSyncDelta(currentVersion)
            if (response.hasUpdates) {
                // Bulk insert/update room tables inside transaction
                db.withTransaction {
                    // Update FLN outcomes, lessons, glossary terms
                    db.syncDao().updateMetadata(
                        SyncMetadataEntity(
                            localContentVersion = response.serverVersion,
                            lastSyncTimestamp = System.currentTimeMillis()
                        )
                    )
                }
            }
            Result.success(true)
        } catch (e: Exception) {
            // Internet is unavailable: Continue completely offline using local Room DB
            Result.failure(e)
        }
    }
}
```
