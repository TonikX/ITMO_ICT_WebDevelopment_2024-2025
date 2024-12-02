import {Module} from "@nestjs/common";
import { SequelizeModule } from "@nestjs/sequelize";
import { UsersModule } from './users/users.module';
import {ConfigModule} from "@nestjs/config";
import * as process from "node:process";
import {User} from "./users/users.model";
import {ArtistsModule} from "./artists/artists.module";
import {Artist} from "./artists/artists.model";
import {UserBlockedArtists} from "./users/user-blocked-artists.model";
import { AuthModule } from './auth/auth.module';
import { FilesModule } from './files/files.module';
import {ServeStaticModule} from "@nestjs/serve-static";
import * as path from 'path'
import {ArtistsAuthModule} from "./artists-auth/artists-auth.module";
import { AlbumsModule } from './albums/albums.module';
import {Album} from "./albums/albums.model";
import {AlbumArtists} from "./albums/album-artists.model";
import {UserFavouriteAlbums} from "./users/user-favourite-albums.model";

@Module({
    controllers: [],
    providers: [],
    imports: [
        ConfigModule.forRoot({
            envFilePath: `.${process.env.NODE_ENV}.env`,
        }),
        ServeStaticModule.forRoot({
            rootPath: path.resolve(__dirname, 'static')
        }),
        SequelizeModule.forRoot({
            dialect: 'postgres',
            host: process.env.POSTGRES_HOST,
            port: Number(process.env.POSTGRES_PORT),
            username: process.env.POSTGRES_USER,
            password: process.env.POSTGRES_PASSWORD,
            database: process.env.POSTGRES_DB,
            autoLoadModels: true,
            models: [User, Artist, UserBlockedArtists, Album, AlbumArtists, UserFavouriteAlbums]
        }),
        UsersModule,
        AuthModule,
        ArtistsModule,
        ArtistsAuthModule,
        FilesModule,
        AlbumsModule,
    ],
})
export class AppModule {}