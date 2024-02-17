<template>
  <q-item>
    <q-input
      dense
      v-model="searchValue"
      @clear="searchValue = ''"
      placeholder="Filter subscriptions"
      clearable
      style="width: 100%"
    >
      <template v-slot:prepend>
        <q-icon name="search" />
      </template>
    </q-input>
  </q-item>
  <div style="height: calc(100% - 56px); overflow-y: scroll">
    <div v-if="contentStore.subscriptionsIsLoading" class="mx-auto">
      <loading-indicator style="width: 40px"></loading-indicator>
    </div>
    <q-list>
      <ChannelListCategory
        v-for="category in subscriptionCategories"
        :key="category?.id ?? null"
        :id="category?.id ?? 0"
        :name="category?.name ?? 'Uncategorized'"
        :subscriptions="
          subscriptionsFiltered.filter(
            (s) => s.category_id === (category?.id ?? null)
          )
        "
        :is-searching="searchValue != ''"
      />
    </q-list>
  </div>
  <q-separator />
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import LoadingIndicator from 'components/LoadingIndicator.vue';
import ChannelListCategory from 'components/ChannelListCategory.vue';
import { useContentStore } from 'stores/content-store';

const contentStore = useContentStore();

const searchValue = ref('');

const subscriptions = computed(() => contentStore.subscriptions);

const subscriptionsFiltered = computed(() => {
  return subscriptions.value.filter((s) =>
    s.publishing_channel.name
      .toLowerCase()
      .includes(searchValue.value.toLowerCase())
  );
});

const subscriptionCategories = computed(() => [
  ...contentStore.subscriptionCategories,
  { id: null, name: 'Uncategorized' },
]);
</script>
