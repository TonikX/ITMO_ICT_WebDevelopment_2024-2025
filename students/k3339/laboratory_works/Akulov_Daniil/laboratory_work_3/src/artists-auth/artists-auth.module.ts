import {forwardRef, Module} from '@nestjs/common';
import {JwtModule} from "@nestjs/jwt";
import * as process from "node:process";
import {ArtistsAuthController} from "./artists-auth.controller";
import {ArtistsAuthService} from "./artists-auth.service";
import {ArtistsModule} from "../artists/artists.module";

@Module({
    controllers: [ArtistsAuthController],
    providers: [ArtistsAuthService],
    imports: [
        forwardRef(() => ArtistsModule),
        JwtModule.register({
            secret: process.env.PRIVATE_KEY || 'secret 123',
            signOptions: {
                expiresIn: '24h'
            }
        })
    ],
    exports: [
        ArtistsAuthService,
        JwtModule
    ]
})
export class ArtistsAuthModule {}
