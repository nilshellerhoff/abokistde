<template>
  <q-item-label header>Subscriptions</q-item-label>
  <q-item>
    <q-input
      outlined
      v-model="searchValue"
      @update:model-value="
        isSearching = true;
        searchDebounced();
      "
      @clear="searchValue = ''"
      placeholder="Search channels"
      clearable
      style="width: 100%"
    >
      <template v-slot:prepend>
        <q-icon name="search" />
      </template>
    </q-input>
  </q-item>
  <div style="height: calc(100% - 72px - 48px); overflow-y: scroll">
    <div v-if="isLoading" class="mx-auto">
      <loading-indicator style="width: 40px"></loading-indicator>
    </div>
    <q-list>
      <ChannelListCategory
        v-for="category in subscriptionCategories"
        :key="category?.id ?? null"
        :name="category?.name ?? 'Uncategorized'"
        :subscriptions="
          subscriptionsFiltered.filter(
            (s) => s.category_id === (category?.id ?? null)
          )
        "
      />
      <q-separator />

      <span v-if="searchValue.trim() !== ''">
        <q-item-label header>Search Results</q-item-label>
        <span v-if="isSearching">
          <q-item class="text-center">
            <loading-indicator
              class="mx-auto"
              style="width: 40px"
            ></loading-indicator>
          </q-item>
        </span>
        <span v-else>
          <q-item class="text-center">
            <q-btn @click="searchOnline">Search on Youtube</q-btn>
          </q-item>
          <ChannelRenderer
            v-for="channel in searchResults"
            :key="channel.id"
            :channel="channel"
            :show-add-subscription="
              !subscriptions.find((s) => s.publishing_channel.id === channel.id)
            "
            @subscribe="subscribe(channel)"
        /></span>
      </span>
    </q-list>
  </div>
  <q-separator />
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import LoadingIndicator from 'components/LoadingIndicator.vue';
import { apiClient } from 'src/util/api';
import ChannelRenderer from 'components/ChannelRenderer.vue';
import _ from 'lodash';
import { PublishingChannel, UserSubscription } from 'src/types/api';
import { uniqOn } from 'src/util/array';
import ChannelListCategory from 'components/ChannelListCategory.vue';

const searchValue = ref('');

const isLoading = ref(0);

const channels = ref([]);
const subscriptions = ref([]);
const subscriptionsFiltered = computed(() => {
  return subscriptions.value.filter((s) =>
    s.publishing_channel.name
      .toLowerCase()
      .includes(searchValue.value.toLowerCase())
  );
});

const subscriptionCategories = computed(() =>
  uniqOn(
    subscriptions.value.map((s) => s.category),
    'id'
  ).sort((a, b) => (a?.name ?? 'zzz' < b?.name ?? 'zzz' ? -1 : 1))
);

const searchResults = ref([]);
const isSearching = ref(false);

const fetchSubscriptions = () => {
  isLoading.value++;
  apiClient
    .get('/user_subscription/')
    .then((response) => {
      subscriptions.value = response.data.results;
      channels.value = response.data.results.map((s) => s.publishing_channel);
    })
    .finally(() => {
      isLoading.value--;
    });
};

const search = () => {
  searchResults.value = [];
  if (searchValue.value.trim() !== '') {
    isSearching.value = true;
    apiClient
      .get('/publishing_channel/', {
        params: {
          search: searchValue.value.trim(),
        },
      })
      .then((response) => {
        searchResults.value = response.data.results;
      })
      .finally(() => {
        isSearching.value = false;
      });
  }
};

const searchDebounced = _.debounce(function () {
  console.log('search debounced');
  search();
}, 500);

const searchOnline = () => {
  searchResults.value = [];
  if (searchValue.value.trim() !== '') {
    isSearching.value = true;
    apiClient
      .get('/search_online/', {
        params: {
          query: searchValue.value.trim(),
        },
      })
      .then((response) => {
        searchResults.value = response.data.data;
        isSearching.value = false;
      })
      .catch(() => {
        isSearching.value = false;
      });
  }
};

const subscribe = (channel: PublishingChannel) => {
  apiClient
    .post('user_subscription/', {
      publishing_channel_id: channel.id,
    })
    .then(() => {
      fetchSubscriptions();
    });
};

fetchSubscriptions();
</script>
