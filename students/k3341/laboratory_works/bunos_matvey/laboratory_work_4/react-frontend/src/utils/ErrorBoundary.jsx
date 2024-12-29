import React from 'react';
import { Result, Button } from 'antd';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, errorInfo: null };
  }
  
  static getDerivedStateFromError(error) {
    return { hasError: true, errorInfo: error };
  }
  
  componentDidCatch(error, errorInfo) {
    console.error('Ошибка в ErrorBoundary:', error, errorInfo);
  }
  
  handleReload = () => {
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <Result
          status="error"
          title="Произошла ошибка"
          subTitle="Что-то пошло не так. Попробуйте обновить страницу."
          extra={[
            <Button type="primary" onClick={this.handleReload}>Обновить</Button>
          ]}
        />
      );
    }
    return this.props.children;
  }
}

export default ErrorBoundary;
