declare module 'vue-router' {
  import type { Router as _Router, RouteRecordRaw as _RouteRecordRaw } from 'vue-router/dist/vue-router'
  export type Router = _Router
  export type RouteRecordRaw = _RouteRecordRaw
  export function useRouter(): Router
  export function createRouter(options: any): Router
  export function createWebHistory(base?: string): any
} 