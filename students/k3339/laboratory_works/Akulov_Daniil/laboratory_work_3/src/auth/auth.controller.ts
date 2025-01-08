import {Body, Controller, Post} from '@nestjs/common';
import {AuthService} from "./auth.service";
import {CreateUserDto} from "../users/dto/create-user.dto";
import {LoginUserDto} from "../users/dto/login-user.dto";
import {ApiOperation, ApiResponse} from "@nestjs/swagger";
import {LoginArtistDto} from "../artists/dto/login-artist.dto";

@Controller('auth')
export class AuthController {
    constructor(private readonly authService: AuthService) {}


    @ApiOperation({summary: 'Login as artist'})
    @ApiResponse({status: 200, type: String})
    @Post('/login')
    login(@Body() userDto: LoginUserDto) {
        return this.authService.login(userDto)
    }

    @ApiOperation({summary: 'Registration new artist'})
    @ApiResponse({status: 200, type: String})
    @Post('/registration')
    registration(@Body() userDto: CreateUserDto) {
        return this.authService.registration(userDto)
    }
}
