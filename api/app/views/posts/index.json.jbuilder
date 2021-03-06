json.array! @posts do |post|
    json.id post.id
    json.user_id post.user_id
    json.content post.content
    json.source_id post.source_id
    json.created_at post.created_at
    json.updated_at post.updated_at

    json.evaluation Evaluation.eval_post(post)
end