<template>
  <q-item clickable @click="toggleExpansion">
    <q-item-section>
      <q-item-label>{{ name }}</q-item-label>
    </q-item-section>
    <q-item-section side>
      <q-btn
        flat
        round
        dense
        :icon="isExpanded ? 'expand_less' : 'expand_more'"
      />
    </q-item-section>
  </q-item>

  <span v-if="isExpanded">
    <ChannelRenderer
      v-for="subscription in subscriptions"
      :key="subscription.id"
      :subscription="subscription"
      show-subscription-settings
      @unsubscribe="$emit('unsubscribe', subscription)"
    />
  </span>
</template>

<script setup lang="ts">
import ChannelRenderer from 'components/ChannelRenderer.vue';
import { ref } from 'vue';

interface Props {
  name: string;
  subscriptions: any[];
}

const props = defineProps<Props>();

const isExpanded = ref(true);

const toggleExpansion = () => (isExpanded.value = !isExpanded.value);
</script>
