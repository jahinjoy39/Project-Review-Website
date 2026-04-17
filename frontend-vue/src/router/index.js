import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ProjectsView from '../views/ProjectsView.vue'
import ProjectDetailView from '../views/ProjectDetailView.vue'
import UploadProjectView from '../views/UploadProjectView.vue'
import LeaderboardView from '../views/LeaderboardView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ModerationView from '../views/ModerationView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/projects', name: 'projects', component: ProjectsView },
  { path: '/projects/:id', name: 'project-detail', component: ProjectDetailView },
  { path: '/upload', name: 'upload', component: UploadProjectView },
  { path: '/leaderboard', name: 'leaderboard', component: LeaderboardView },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/register', name: 'register', component: RegisterView },
  { path: '/moderation', name: 'moderation', component: ModerationView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router