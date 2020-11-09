<template>
  <div>
    <b-table striped hover :items="items" :fields="fields">
      <template v-slot:cell(name)="row">
        <b-form-input v-model="row.item.name" />
      </template>
      <template v-slot:cell(age)="row">
        <b-form-input v-model="row.item.age" />
      </template>
    </b-table>
    {{ items }}
  </div>
</template>

<style>
body {
  padding: 1rem;
}
</style>

<script>
export default {
  data() {
    return {
      fields: { Name: 'name', Age: 'age' },
      items: [
        { name: 'Joe', age: 33 },
        { name: 'Sue', age: 77 },
      ],
    }
  },
}
</script>
