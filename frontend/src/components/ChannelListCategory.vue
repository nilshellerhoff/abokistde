<template>
  <q-expansion-item
    v-if="subscriptions.length > 0"
    :label="name"
    expand-separator
    :group="isSearching ? null : 'subscriptionCategories'"
    v-model="isExpanded"
    :to="isSearching ? null : `/feed/${id}`"
  >
    <ChannelRenderer
      v-for="subscription in subscriptions"
      :key="subscription.id"
      :subscription="subscription"
      show-subscription-settings
      @unsubscribe="$emit('unsubscribe', subscription)"
    />
  </q-expansion-item>
</template>

<script setup lang="ts">
import ChannelRenderer from 'components/ChannelRenderer.vue';
import { ref, watch } from 'vue';

interface Props {
  id: number;
  name: string;
  subscriptions: any[];
  isSearching: boolean;
}

const props = defineProps<Props>();

const isExpanded = ref(false);

watch(
  () => props.isSearching,
  () => {
    isExpanded.value = props.isSearching;
  }
);
</script>
