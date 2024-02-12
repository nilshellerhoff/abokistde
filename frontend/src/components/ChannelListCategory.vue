<template>
  <q-expansion-item :label="name" expand-separator>
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
import { ref } from 'vue';

interface Props {
  name: string;
  subscriptions: any[];
}

const props = defineProps<Props>();
</script>
