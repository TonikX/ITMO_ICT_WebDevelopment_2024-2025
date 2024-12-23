module.exports = {
  root: true,
  env: {
    node: true,
    browser: true,
    es2021: true
  },
  extends: [
    'plugin:vue/vue3-essential', 
    'eslint:recommended'
  ],
  parserOptions: {
    parser: '@babel/eslint-parser', 
    ecmaVersion: 2021,
    sourceType: 'module'
  },
  plugins: [
    'vue'
  ],
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    // Добавьте или измените другие правила по необходимости
  }
};
