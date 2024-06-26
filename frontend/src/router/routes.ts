import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', redirect: '/feed' },
      {
        path: 'feed',
        name: 'feed',
        component: () => import('pages/FeedPage.vue'),
      },
      {
        path: 'feed/:id',
        name: 'feedCategory',
        component: () => import('pages/FeedCategoryPage.vue'),
      },
      {
        path: 'favorites',
        name: 'favorites',
        component: () => import('pages/FavoritesPage.vue'),
      },
      {
        path: 'channel/:id',
        name: 'channel',
        component: () => import('pages/ChannelPage.vue'),
      },
      {
        path: 'search',
        name: 'search',
        component: () => import('pages/SearchPage.vue'),
      },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
