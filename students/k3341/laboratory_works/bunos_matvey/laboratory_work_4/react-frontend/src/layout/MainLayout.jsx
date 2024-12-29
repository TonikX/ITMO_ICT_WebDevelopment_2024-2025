// src/layout/MainLayout.jsx
import React, { useContext, useState } from "react";
import { Layout, Menu, Typography } from "antd";
import { Link, useLocation } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const { Header, Sider, Content, Footer } = Layout;
const { Title } = Typography;

function MainLayout({ children }) {
  const { authToken, logout } = useContext(AuthContext);
  const location = useLocation();
  const [collapsed, setCollapsed] = useState(false);

  const secureMenuItems = [
    { key: "authors", label: <Link to="/authors">Авторы</Link> },
    {
      key: "reading-rooms",
      label: <Link to="/reading-rooms">Читальные залы</Link>,
    },
    { key: "books", label: <Link to="/books">Книги</Link> },
    { key: "readers", label: <Link to="/readers">Читатели</Link> },
    {
      key: "books-report",
      label: <Link to="/books/report">Отчёт по книгам</Link>,
    },
  ];

  const commonMenuItems = [
    {
      key: "home",
      label: <Link to="/">Главная</Link>,
    },
  ];

  const authMenuItems = authToken
    ? [
        {
          key: "logout",
          label: "Выйти",
          onClick: async () => {
            await logout();
          },
        },
      ]
    : [
        {
          key: "login",
          label: <Link to="/login">Войти</Link>,
        },
        {
          key: "register",
          label: <Link to="/register">Регистрация</Link>,
        },
      ];

  const menuItems = [
    ...commonMenuItems,
    ...(authToken ? secureMenuItems : []),
    ...authMenuItems,
  ];

  const pathKeyMap = {
    "/": "home",
    "/authors": "authors",
    "/reading-rooms": "reading-rooms",
    "/books": "books",
    "/readers": "readers",
    "/book-assignments": "book-assignments",
    "/book-rooms": "book-rooms",
    "/login": "login",
    "/register": "register",
  };

  const currentKey = Object.keys(pathKeyMap).find((key) =>
    location.pathname.startsWith(key)
  );
  const selectedKey = currentKey || "home";

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Sider collapsible collapsed={collapsed} onCollapse={setCollapsed}>
        <div
          style={{
            height: 64,
            margin: 16,
            display: "flex",
            alignItems: "center",
            justifyContent: collapsed ? "center" : "flex-start",
          }}
        >
          <Title
            level={4}
            style={{
              color: "white",
              margin: 0,
            }}
          >
            {collapsed ? "Lib" : "Library"}
          </Title>
        </div>

        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[selectedKey]}
          items={menuItems}
        />
      </Sider>

      <Layout className="site-layout">
        <Header
          style={{
            background: "#fff",
            padding: "0 16px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          <Title level={3} style={{ margin: 0 }}>
            Library
          </Title>
        </Header>

        <Content style={{ margin: "16px" }}>{children}</Content>

        <Footer style={{ textAlign: "center" }}>
          © {new Date().getFullYear()} Library
        </Footer>
      </Layout>
    </Layout>
  );
}

export default MainLayout;
