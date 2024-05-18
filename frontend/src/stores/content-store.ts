import { defineStore } from 'pinia';
import {
  GenericPaginationResponse,
  PublishingChannel,
  SubscriptionCategory,
  SubscriptionCategoryResponse,
  UserSubscription,
  UserSubscriptionUpdate,
} from 'src/types/api';
import { apiClient } from 'src/util/api';

interface ContentStore {
  subscriptionCategories: SubscriptionCategory[];
  subscriptions: UserSubscription[];
  subscriptionsIsLoading: boolean;
}

export const useContentStore = defineStore('content', {
  state: (): ContentStore => ({
    subscriptionCategories: [],
    subscriptions: [],
    subscriptionsIsLoading: false,
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
    getSubscriptionByChannel(
      channel: PublishingChannel
    ): UserSubscription | undefined {
      return this.subscriptions.find(
        (s) => s.publishing_channel.id == channel.id
      );
    },
    // adders
    addSubscription(subscription: UserSubscriptionUpdate) {
      return apiClient.post('/user_subscription/', subscription).then(() => {
        this.loadSubscriptions();
      });
    },
    addSubscriptionCategory(category: Partial<SubscriptionCategory>) {
      return apiClient.post('/subscription_category/', category).then(() => {
        this.loadCategories();
      });
    },
    // updaters
    updateSubscription(id: number, subscription: UserSubscriptionUpdate) {
      return apiClient
        .put(`/user_subscription/${id}/`, subscription)
        .then(() => {
          this.loadSubscriptions();
        });
    },
    // removers
    removeSubscription(id: number) {
      return apiClient.delete(`/user_subscription/${id}/`).then(() => {
        this.loadSubscriptions();
      });
    },
    // loaders
    loadCategories() {
      return apiClient
        .get<SubscriptionCategoryResponse>('/subscription_category/')
        .then((response) => {
          this.subscriptionCategories = response.data.results;
        });
    },
    loadSubscriptions() {
      this.subscriptionsIsLoading = true;
      return apiClient
        .get<GenericPaginationResponse<UserSubscription>>('/user_subscription/')
        .then((response) => {
          this.subscriptions = response.data.results;
        })
        .finally(() => {
          this.subscriptionsIsLoading = false;
        });
    },
  },
});
