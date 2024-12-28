// src/views/Blog.vue
<template>
    <v-container>
    <v-row>
      <!-- Add Post Button -->
      <v-col cols="12">
        <v-btn
          color="primary"
          @click="dialog = true"
        >
          Create New Post
        </v-btn>
      </v-col>

      <!-- Filters -->
      <v-col cols="12">
        <v-card class="mb-4">
          <v-card-text>
            <v-row>
              <v-col cols="12" sm="6">
                <v-select
                  v-model="selectedCategory"
                  :items="categories"
                  label="Category"
                  clearable
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="search"
                  label="Search"
                  prepend-icon="mdi-magnify"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Blog Posts -->
      <v-col v-for="post in filteredPosts" :key="post.id" cols="12" md="6">
        <v-card class="mb-4">
          <v-img
            v-if="post.image_url"
            :src="post.image_url"
            height="200"
            cover
          ></v-img>
          
          <v-card-title>{{ post.title }}</v-card-title>
          
          <v-card-text>
            <div class="mb-2">
              <v-chip small>{{ post.category }}</v-chip>
              <span class="ml-2 caption">
                by {{ post.author.username }} on {{ formatDate(post.created_at) }}
              </span>
            </div>
            <div>{{ truncateContent(post.content) }}</div>
          </v-card-text>

          <v-card-actions>
            <v-btn
              text
              color="primary"
              @click="viewFullPost(post)"
            >
              Read More
            </v-btn>
            <v-spacer></v-spacer>
            <template v-if="isAuthor(post)">
              <v-btn icon @click="editPost(post)">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn icon @click="deletePost(post)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Create/Edit Dialog -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          {{ editingPost ? 'Edit Post' : 'Create New Post' }}
        </v-card-title>
        
        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="postForm.title"
              label="Title"
              required
            ></v-text-field>
            
            <v-textarea
              v-model="postForm.content"
              label="Content"
              required
            ></v-textarea>
            
            <v-text-field
              v-model="postForm.image_url"
              label="Image URL"
            ></v-text-field>
            
            <v-select
              v-model="postForm.category"
              :items="categories"
              label="Category"
              required
            ></v-select>
          </v-form>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="grey darken-1"
            text
            @click="closeDialog"
          >
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            @click="savePost"
            :loading="loading"
            :disabled="!valid || loading"
          >
            {{ editingPost ? 'Update' : 'Create' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Full Post Dialog -->
    <v-dialog v-model="fullPostDialog" max-width="800px">
      <v-card v-if="selectedPost">
        <v-img
          v-if="selectedPost.image_url"
          :src="selectedPost.image_url"
          height="300"
          cover
        ></v-img>
        
        <v-card-title class="headline">{{ selectedPost.title }}</v-card-title>
        
        <v-card-text>
          <div class="mb-4">
            <v-chip small>{{ selectedPost.category }}</v-chip>
            <span class="ml-2 caption">
              by {{ selectedPost.author.username }} on {{ formatDate(selectedPost.created_at) }}
            </span>
          </div>
          <div class="body-1">{{ selectedPost.content }}</div>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="grey darken-1"
            text
            @click="fullPostDialog = false"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import axios from 'axios'

export default {
  name: 'Blog',
  data: () => ({
    dialog: false,
    fullPostDialog: false,
    valid: false,
    loading: false,
    search: '',
    selectedCategory: null,
    selectedPost: null,
    editingPost: null,
    categories: ['Fitness', 'Nutrition', 'Motivation', 'Recovery', 'Equipment'],
    postForm: {
      title: '',
      content: '',
      image_url: '',
      category: ''
    }
  }),
  computed: {
    ...mapState(['posts', 'user']),
    // Filter posts based on search and category
    filteredPosts() {
      return this.posts.filter(post => {
        const matchesSearch = !this.search || 
          post.title.toLowerCase().includes(this.search.toLowerCase()) ||
          post.content.toLowerCase().includes(this.search.toLowerCase())
        
        const matchesCategory = !this.selectedCategory || 
          post.category === this.selectedCategory
        
        return matchesSearch && matchesCategory
      })
    }
  },
  methods: {
    ...mapActions(['fetchPosts']),
    
    // Format date to a readable string
    formatDate(date) {
      return new Date(date).toLocaleDateString()
    },
    
    // Truncate post content for preview
    truncateContent(content) {
      return content.length > 200 ? content.substring(0, 200) + '...' : content
    },
    
    // Check if current user is the author of the post
    isAuthor(post) {
      return this.user && post.author.id === this.user.id
    },
    
    // Show full post in dialog
    viewFullPost(post) {
      this.selectedPost = post
      this.fullPostDialog = true
    },
    
    // Initialize edit post form
    editPost(post) {
      this.editingPost = post
      this.postForm = { ...post }
      this.dialog = true
    },
    
    // Reset and close dialog
    closeDialog() {
      this.dialog = false
      this.editingPost = null
      this.postForm = {
        title: '',
        content: '',
        image_url: '',
        category: ''
      }
      this.$refs.form.reset()
    },
    
    // Save new post or update existing one
    async savePost() {
      this.loading = true
      try {
        if (this.editingPost) {
          // Update existing post
          await axios.put(`blogs/${this.editingPost.id}/`, this.postForm)
        } else {
          // Create new post
          await axios.post('blogs/create/', this.postForm)
        }
        // Refresh posts list
        await this.fetchPosts()
        this.closeDialog()
        this.$store.commit('SET_SNACKBAR', {
          text: `Post ${this.editingPost ? 'updated' : 'created'} successfully!`,
          color: 'success'
        })
      } catch (error) {
        console.error('Error saving post:', error)
        this.$store.commit('SET_SNACKBAR', {
          text: 'Error saving post',
          color: 'error'
        })
      } finally {
        this.loading = false
      }
    },
    
    // Delete post
    async deletePost(post) {
      if (!confirm('Are you sure you want to delete this post?')) return
      
      try {
        await axios.delete(`blogs/${post.id}/`)
        await this.fetchPosts()
        this.$store.commit('SET_SNACKBAR', {
          text: 'Post deleted successfully!',
          color: 'success'
        })
      } catch (error) {
        console.error('Error deleting post:', error)
        this.$store.commit('SET_SNACKBAR', {
          text: 'Error deleting post',
          color: 'error'
        })
      }
    }
  },
  async created() {
    try {
      await this.fetchPosts()
    } catch (error) {
      console.error('Error fetching posts:', error)
    }
  }
}
</script>