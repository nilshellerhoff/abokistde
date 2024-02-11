import { defineStore } from 'pinia';
import { useLocalStorage } from '@vueuse/core';

import { Quasar, Platform, Dark } from 'quasar';
import {
  SubscriptionCategory,
  EpisodeResponse,
  SubscriptionCategoryResponse,
} from 'src/types/api';
import { apiClient } from 'src/util/api';

interface ContentStore {
  subscriptionCategories: SubscriptionCategory[];
}

export const useContentStore = defineStore('content', {
  state: (): ContentStore => ({
    subscriptionCategories: [],
  }),
  actions: {
    init() {
      this.loadCategories();
    },
    loadCategories() {
      apiClient
        .get<SubscriptionCategoryResponse>('/subscription_category/')
        .then((response) => {
          this.subscriptionCategories = response.data.results;
        });
    },
  },
});
