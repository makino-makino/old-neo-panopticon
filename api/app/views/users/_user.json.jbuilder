json.extract! user, :id, :name, :bio, :icon
# :id, :name, :image, :created_at, :updated_at, :bio
json.evaluation PostEvaluation.eval_user(user)
# json.url user_url(user, format: :json)
