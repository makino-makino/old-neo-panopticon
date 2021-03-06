class PostsController < ApplicationController
  before_action :authenticate_user!
  before_action :set_post, only: [:eval, :show, :update, :destroy]

  # GET /posts
  # GET /posts.json
  def index
    params.permit(:tl, :numbers, :start_created, :start_id, :user_id)

    if not params[:numbers].nil?
      numbers = params[:numbers].to_i
    else
      numbers = 10
    end

    if not params[:start_id].nil?
      start_id = params[:start_id]
    else
      start_id = 0
    end

    if not params[:start_created].nil?
      start_created = params[:start_created]
    else
      start_created = 0
    end

    # set values
    if params[:tl].nil?
      # デバッグ用
      @posts = Post.last(10)
      render :for_debug, status: :ok, location: @post
      return
    elsif params[:tl] == "global"
      users = User.all
    elsif params[:tl] == "local"
      followings = Following.where(from: current_user).first()
      
      if followings.nil?
        @posts = []
        return
      end

      users = User.where(id: followings.to_id)
    elsif params[:tl] == "user" and not params[:user_id].nil?
      @posts = Post.userTL(params[:user_id], numbers, start_id, start_created)
      return
    end
 
    @posts = Post.tl(params[:tl], users, numbers, start_id, start_created)
    render :for_debug, status: :ok, location: @post
    
    return 
  end

  # GET /posts/1
  # GET /posts/1.json
  def show
    @score = Evaluation.eval_post(@post)
  end

  # POST /posts
  # POST /posts.json
  def create
    params.permit(:content, :souce_id)

    if params[:source_id].nil?
      # 普通のポスト
      @post = Post.new(content: params[:content])
    elsif not Post.find(params[:source_id]).nil?
      # リツイート
      @post = Post.new(content: params[:content], source_id: params[:source_id])
    end

    @post.user = current_user

    if @post.save
      render :show, status: :created, location: @post
    else
      render json: @post.errors, status: :unprocessable_entity
    end
  end

  def eval
    params.require(:score)
    params.permit(:score)
    score = params[:score]

    # TODO: Validation

    @post = Post.find(params['id'])

    # validate
    if not (evaluation = Evaluation.find_by(post_id: @post.id, user_id: current_user.id)).nil? 
      @evaluation = evaluation
      render :eval
    else
      @evaluation = Evaluation.new(post: @post, user:current_user, score: score)

      if @evaluation.save
        render :eval
      else
        render json: @evaluation.errors, status: :unprocessable_entity
      end
    end

  end

  # PATCH/PUT /posts/1
  # PATCH/PUT /posts/1.json
  # def update
  #   if @post.update(post_params)
  #     render :show, status: :ok, location: @post
  #   else
  #     render json: @post.errors, status: :unprocessable_entity
  #   end
  # end

  # DELETE /posts/1
  # DELETE /posts/1.json
  # def destroy
  #   @post.destroy
  # end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_post
      @post = Post.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def post_params
      params.require(:content)
      params.permit(:content) #, :type, :souce_id)
    end
end
