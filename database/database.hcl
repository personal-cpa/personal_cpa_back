schema "personal_cpa" {}

table "dummy" {
  schema = schema.personal_cpa
  comment = "hi"

  column "id" {
    type = int
    null = false
    auto_increment = true
  }

  primary_key {
    columns = [column.id]
  }
}