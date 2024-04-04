<template>
  <q-expansion-item
    v-if="subscriptions.length > 0"
    expand-separator
    :group="isSearching ? null : 'subscriptionCategories'"
    v-model="isExpanded"
    :to="isSearching ? null : `/feed/${id}`"
    dense
  >
    <template #header>
      <q-item-section>
        <q-item-label header>
          {{ name }}
        </q-item-label>
      </q-item-section>
      <q-item-section side>
        <q-btn icon="play_arrow" flat dense />
      </q-item-section>
    </template>
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
