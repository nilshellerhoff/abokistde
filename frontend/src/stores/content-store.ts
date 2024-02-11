import { defineStore } from 'pinia';
import {
  GenericPaginationResponse,
  SubscriptionCategory,
  SubscriptionCategoryResponse,
  UserSubscription,
  UserSubscriptionUpdate,
} from 'src/types/api';
import { apiClient } from 'src/util/api';

interface ContentStore {
  subscriptionCategories: SubscriptionCategory[];
  subscriptions: UserSubscription[];
}

export const useContentStore = defineStore('content', {
  state: (): ContentStore => ({
    subscriptionCategories: [],
    subscriptions: [],
  }),
  actions: {
    init() {
      this.loadCategories();
      this.loadSubscriptions();
    },
    // getters
    getSubscriptionById(id: number) {
      return this.subscriptions.find((s) => s.id === id);
    },
    // adders
    addSubscriptionCategory(category: Partial<SubscriptionCategory>) {
      apiClient.post('/subscription_category/', category).then(() => {
        this.loadCategories();
      });
    },
    // updaters
    updateSubscription(id: number, subscription: UserSubscriptionUpdate) {
      apiClient.put(`/user_subscription/${id}/`, subscription).then(() => {
        this.loadSubscriptions();
      });
    },
    // removers
    removeSubscription(id: number) {
      apiClient.delete(`/user_subscription/${id}/`).then(() => {
        this.loadSubscriptions();
      });
    },
    // loaders
    loadCategories() {
      apiClient
        .get<SubscriptionCategoryResponse>('/subscription_category/')
        .then((response) => {
          this.subscriptionCategories = response.data.results;
        });
    },
    loadSubscriptions() {
      apiClient
        .get<GenericPaginationResponse<UserSubscription>>('/user_subscription/')
        .then((response) => {
          this.subscriptions = response.data.results;
        });
    },
  },
});
