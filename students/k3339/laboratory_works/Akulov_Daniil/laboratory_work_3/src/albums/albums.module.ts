import {forwardRef, Module} from '@nestjs/common';
import { AlbumsService } from './albums.service';
import { AlbumsController } from './albums.controller';
import {SequelizeModule} from "@nestjs/sequelize";
import {Album} from "./albums.model";
import {Artist} from "../artists/artists.model";
import {AlbumArtists} from "./album-artists.model";
import {FilesModule} from "../files/files.module";
import {ArtistsModule} from "../artists/artists.module";
import {ArtistsAuthModule} from "../artists-auth/artists-auth.module";
import {User} from "../users/users.model";
import {UserFavouriteAlbums} from "../users/user-favourite-albums.model";

@Module({
    controllers: [AlbumsController],
    providers: [AlbumsService],
    imports: [
        SequelizeModule.forFeature([Album, AlbumArtists, Artist, User, UserFavouriteAlbums]),
        forwardRef(() => ArtistsModule),
        FilesModule,
        ArtistsAuthModule
    ],
    exports: [
        AlbumsService,
    ]
})
export class AlbumsModule {}
