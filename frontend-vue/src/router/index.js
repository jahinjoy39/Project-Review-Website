import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ProjectsView from '../views/ProjectsView.vue'
import ProjectDetailView from '../views/ProjectDetailView.vue'
import UploadProjectView from '../views/UploadProjectView.vue'
import LeaderboardView from '../views/LeaderboardView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/login', component: LoginView },
  { path: '/register', component: RegisterView },
  { path: '/projects', component: ProjectsView },
  { path: '/projects/:id', component: ProjectDetailView },
  { path: '/upload', component: UploadProjectView },
  { path: '/leaderboard', component: LeaderboardView }
]

export default createRouter({ history: createWebHistory(), routes })
